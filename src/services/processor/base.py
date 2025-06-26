import abc

from base_sync.base_module import ClassesLoggerAdapter
from services.processor.algorithms import Algorithms
from models import Params


class BaseProcessor(abc.ABC):
    def __init__(self):
        self._logger = ClassesLoggerAdapter.create(self)

    @abc.abstractmethod
    def process(self, src_file: str, params: Params):
        pass