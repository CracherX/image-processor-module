from base_sync.services import RabbitService
from base_sync.services.filer import FilerExchangeService
from config import config
from services import TasksWorker
from services.tasks import TasksService
from .connections import pg


def rabbit() -> RabbitService:
    return RabbitService(config.rabbit)

def filer() -> FilerExchangeService:
    return FilerExchangeService(
        url=config.filer.url,
        con_timeout=config.filer.connect_timeout,
        read_timeout=config.filer.read_timeout,
        server_save_path=config.filer.server_save_path,
        auto_comment=config.filer.auto_comment,
    )

def tasks() -> TasksService:
    return TasksService(
        rabbit=rabbit(),
        pg=pg.acquire_session()
    )

def tasks_mule() -> TasksWorker:
    """."""
    return TasksWorker(
        rabbit=rabbit(),
        pg_connection=pg.acquire_session(),
        filer=filer(),
        upload_dir=config.upload_dir
    )