import dataclasses as dc
import typing
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import Index

from base_sync.base_module import BaseOrmMappedModel, Model, ValuedEnum

SCHEMA_NAME = 'public'


class TaskStatus(ValuedEnum):
    NEW = 'new'
    PROCESSING = 'processing'
    ERROR = 'error'
    DONE = 'done'


@dc.dataclass
class Task(BaseOrmMappedModel):
    __tablename__ = 'tasks'
    __table_args__ = (
        Index('ix_files_path', 'path'),
        {'schema': SCHEMA_NAME}
    )

    id: int = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.Integer, primary_key=True, index=True)}
    )
    file_id: int = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.Integer, nullable=False)}
    )
    algorithm: str = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.String(30), nullable=False)}
    )
    params: typing.Optional[dict] = dc.field(
        default_factory=dict,
        metadata={'sa': sa.Column(sa.JSON, nullable=True)}
    )
    status: TaskStatus = dc.field(
        default=TaskStatus.NEW,
        metadata={
            'sa': sa.Column(
                sa.Enum(TaskStatus, name='tt_processor_status',
                        schema=SCHEMA_NAME)
            )
        }
    )
    duration: float = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.Float, nullable=True)}
    )
    created_at: datetime = dc.field(
        default_factory=datetime.utcnow,
        metadata={'sa': sa.Column(sa.DateTime, nullable=False)}
    )
    updated_at: typing.Optional[datetime] = dc.field(
        default=None,
        metadata={'sa': sa.Column(sa.DateTime, nullable=True)}
    )


BaseOrmMappedModel.REGISTRY.mapped(Task)


@dc.dataclass
class Params(Model):
    target_projection: typing.Optional[str] = dc.field(default=None)
    scale_x: typing.Optional[int] = dc.field(default=None)
    scale_y: typing.Optional[int] = dc.field(default=None)