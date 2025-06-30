import os
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Session as PGSession

from base_sync.base_module import BaseMule, ClassesLoggerAdapter, sa_operator, ModuleException
from base_sync.models.rabbit import TaskIdentMessageModel
from base_sync.services import RabbitService
from base_sync.services.filer import FilerExchangeService
from models import Task, TaskStatus, Params
from base_sync.models import Algorithms
from .processor import ProcessorFactory


class TasksWorker(BaseMule):
    def __init__(
            self,
            pg_connection: PGSession,
            rabbit: RabbitService,
            filer: FilerExchangeService,
            upload_dir: str,
    ):
        self._pg = pg_connection
        self._rabbit = rabbit
        self._filer_exchange = filer
        self._upload_dir = upload_dir
        self._logger = ClassesLoggerAdapter.create(self)

    def _get_task(self, task_id: int) -> Task | None:
        """Получение задачи из БД"""
        with self._pg.begin():
            task: Task = self._pg.execute(
                sa.select(Task).filter(
                    sa.and_(
                        sa_operator.eq(Task.id, task_id),
                        sa_operator.in_(
                            Task.status,
                            [
                                TaskStatus.NEW,
                                # В случае ручного восстановления работы
                                TaskStatus.PROCESSING
                            ]
                        )
                    )
                ).limit(1)
            ).scalar()
            if not task:
                return

            task.status = TaskStatus.PROCESSING
            task.updated_at = datetime.now()
            self._pg.merge(task)
            return task.reload()

    def _update_status(self, task: Task, status: TaskStatus):
        """Обновление статуса задачи"""
        task.status = status
        updated = datetime.now()
        task.duration = (updated - task.updated_at).total_seconds()
        task.updated_at = updated
        self._logger.info(
            'Изменение статуса задачи',
            extra={'task_id': task.id, 'status': task.status}
        )
        with self._pg.begin():
            if self._pg.get(Task, task.id,
                            with_for_update=True):
                self._pg.merge(task)  # TODO: добавить обработку в случае потери задачи или убрать условие
                return task.reload()  ## (потому что не найти её в таком контексте это очень странно)

    def _work_dir(self, task_id: int) -> str:
        """Создание временной директории"""
        temp_dir = os.path.join(self._upload_dir, str(task_id))
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    def _handle(self, task: Task):
        """Обработка задачи"""
        self._logger.info(
            'Обработка задачи',
            extra={
                'task': task.id
            }
        )
        task = Task.load(task.dump())
        params = Params.load(task.params or {})
        temp_dir = self._work_dir(task.id)
        file_path = self._filer_exchange.download_file(task.file_id, temp_dir)

        processor = ProcessorFactory.create(Algorithms(task.algorithm))
        result = processor.process(file_path, params)
        self._filer_exchange.upload_file(result)
        self._update_status(task, TaskStatus.DONE)

    def _handle_message(self, message: TaskIdentMessageModel, **_):
        """Обработка сообщения от брокера"""
        task_id = message.payload.task_id
        task = self._get_task(task_id)
        if not task:
            self._logger.warn('Задача не найдена', extra={'task_id': task_id})
            return

        try:
            self._handle(task)
        except Exception as e:
            exc_data = {'e': e}
            if isinstance(e, ModuleException):
                exc_data.update(e.data)
            self._logger.critical(
                'Ошибка верхнего уровня обработчика задачи',
                extra=exc_data, exc_info=True
            )
            self._update_status(task, TaskStatus.ERROR)

    def run(self):
        """Запуск прослушивания очереди брокера сообщений"""
        self._rabbit.run_consume(self._handle_message, TaskIdentMessageModel)
