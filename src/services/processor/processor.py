import typing as t

from base_sync.base_module import ModuleException
from base_sync.models import Algorithms
from .base import BaseProcessor
from .projectror import Projector
from .scaler import Scaler


class ProcessorFactory:
    _registry: t.Dict[Algorithms, type[BaseProcessor]] = {
        Algorithms.PROJECTION: Projector,
        Algorithms.SCALING: Scaler,
    }

    @classmethod
    def create(cls, algorithm: Algorithms) -> BaseProcessor:
        processor_cls = cls._registry.get(algorithm)
        if not processor_cls:
            raise ModuleException('Не удалось определить тип алгоритма', code=400)
        return processor_cls()
