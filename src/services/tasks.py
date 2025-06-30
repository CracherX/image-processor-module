import dataclasses as dc
import typing as t

from sqlalchemy.orm import Session as PGSession

from base_sync.base_module import Model, ClassesLoggerAdapter
from base_sync.base_module import ModuleException
from base_sync.models.rabbit import TaskIdentMessageModel
from base_sync.services import RabbitService
from models import Task, TaskStatus


@dc.dataclass
class TaskCreationModel(Model):
    file_id: int = dc.field()
    algorithm: str = dc.field()
    params: dict = dc.field(default_factory=dict)


class TasksService:
    def __init__(
            self,
            rabbit: RabbitService,
            pg: PGSession
    ):
        self._rabbit = rabbit
        self._logger = ClassesLoggerAdapter.create(self)
        self._pg = pg

    def create_task(self, data) -> Task:
        self._logger.info(
            'Создание задачи',
            extra=data
        )
        try:
            data = TaskCreationModel.load(data)
        except Exception:
            raise ModuleException(
                "Ошибка заполнения тела запроса. Убедитесь что алгоритм указан верно",
                code=400,
            )
        task = Task(
            file_id=data.file_id,
            algorithm=data.algorithm,
            params=data.params
        )

        with self._pg.begin():
            self._pg.add(task)

        message = TaskIdentMessageModel.lazy_load(
            TaskIdentMessageModel.T(task.id)
        )
        published = self._rabbit.publish(message)
        if published:
            return task

        with self._pg.begin():
            task.status = TaskStatus.ERROR
        self._logger.error(
            'Ошибка отправления задачи в Rabbit',
            extra=data.dump()
        )
        raise ModuleException(
            'Не удалось отправить задачу на обработку',
            code=502
        )

    def get_task(self, task_id: int) -> Task:
        self._logger.info(
            'Получение задачи по ID',
            extra={
                'task_id': task_id,
            }
        )
        with self._pg.begin():
            task = self._pg.query(Task).filter(Task.id == task_id).first()
            if task:
                return task
            self._logger.info(
                'Задача с таким ID не найден',
                extra={
                    'task_id': task_id,
                }
            )
            raise ModuleException(
                'Задача с таким ID не найдена',
                code=404
            )

    def get_list_tasks(
            self,
            page: str = 1,
            page_size: str = 100
    ) -> t.List[Task]:
        self._logger.info(
            'Запрошен список задач',
            extra={
                'page': page,
                'page_size': page_size
            }
        )
        try:
            page = int(page)
            page_size = int(page_size)
        except:
            self._logger.info(
                'Ошибка в параметрах URL',
                extra={
                    'page': page,
                    'page_size': page_size
                }
            )
            raise ModuleException(
                'Параметры не являются числами или не указаны вовсе',
                code=400
            )

        offset = (page - 1) * page_size
        with self._pg.begin():
            query = self._pg.query(Task)
            return query.offset(offset).limit(page_size).all()
