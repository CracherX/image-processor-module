import abc

from base_sync.base_module import ClassesLoggerAdapter


class BaseProcessor(abc.ABC):
    ALGORITHM: str

    def __init__(self):
        self._logger = ClassesLoggerAdapter.create(self)

    @abc.abstractmethod
    def process(self, src_file: str, params):
        pass
