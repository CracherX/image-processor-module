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
    params: t.Optional[dict] = dc.field(default=None)  # TODO: по параметрам узнать еще


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
        data = TaskCreationModel.load(data)

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
        raise ModuleException(
            'Не удалось отправить задачу на обработку',
            code=502
        )
