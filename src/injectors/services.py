from base_sync.services import FilesStorageService
from base_sync.services import RabbitService
from config import config
from services import TasksWorker
from services.processor import Projector, Scaler, ProcessorFactoryService
from services.tasks import TasksService
from .connections import pg


def rabbit() -> RabbitService:
    return RabbitService(config.rabbit)


def filer() -> FilesStorageService:
    return FilesStorageService(
        url=config.filer.url,
        con_timeout=config.filer.connect_timeout,
        read_timeout=config.filer.read_timeout,
        server_save_path=config.filer.server_save_path,
        auto_comment=config.filer.auto_comment,
    )


def processsor_factory() -> ProcessorFactoryService:
    return ProcessorFactoryService(
        [
            Projector,
            Scaler,
        ]
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
        processor=processsor_factory(),
        work_dir=config.work_dir,
    )
