import typing as t

from base_sync.base_module import ModuleException
from .base import BaseProcessor


class ProcessorFactoryService:

    def __init__(self, processors: t.List[type[BaseProcessor]]):
        self._processors = processors

    def create(self, algorithm: str) -> BaseProcessor:
        for cls in self._processors:
            if cls.ALGORITHM == algorithm:
                return cls()
        raise ModuleException('Не удалось определить тип алгоритма', code=400)
