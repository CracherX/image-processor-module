from base_sync.services import RabbitService
from config import config
from services.tasks import TasksService
from .connections import pg


def rabbit() -> RabbitService:
    return RabbitService(config.rabbit)


def tasks() -> TasksService:
    return TasksService(
        rabbit=rabbit(),
        pg=pg
    )
