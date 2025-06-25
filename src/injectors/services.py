from base_sync.services import RabbitService
from base_sync.services.filer import FilerExchangeService
from config import config
from services.tasks import TasksService
from .connections import pg


def rabbit() -> RabbitService:
    return RabbitService(config.rabbit)

def filer() -> FilerExchangeService:
    return FilerExchangeService(
        url=config.filer.url,
        con_timeout=config.filer.connect_timeout,
        read_timeout=config.filer.read_timeout,
    )

def tasks() -> TasksService:
    return TasksService(
        rabbit=rabbit(),
        pg=pg
    )
