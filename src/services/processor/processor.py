from base import BaseProcessor
import typing as t

from projectror import Projector
from scaler import Scaler


class SatellitesService:
    """."""

    _PROCESSOR_CLS = [
        Projector,
        Scaler
    ]

    def __init__(self, storage_dir: str):
        """."""
        self._storage_dir = storage_dir
        self._processors: t.Dict[SourceType, BaseProcessor] = {
            s.SOURCE_TYPE: s(self._storage_dir) for s in self._PROCESSOR_CLS
        }

    def process(self, source_type: SourceType) -> BaseSatellite:
        """Определение спутника по изображению"""

        sat_cls = self._processors.get(source_type)
        if not sat_cls:
            raise ModuleException('Не удалось определить тип снимка', code=400)

        return sat_cls
