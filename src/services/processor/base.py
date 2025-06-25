import abc

from base_sync.base_module import ClassesLoggerAdapter
from services.processor.algorithms import Algorithms
from models import Params


class BaseProcessor(abc.ABC):
    def __init__(self, algorithm: Algorithms):
        self._logger = ClassesLoggerAdapter.create(self)
        self._algorithm = algorithm

    @abc.abstractmethod
    def process(self, params: Params):
        pass