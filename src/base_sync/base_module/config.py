import dataclasses as dc
import os

from .model import Model


@dc.dataclass
class PgConfig(Model):
    """."""

    host: str = dc.field()
    port: int = dc.field()
    user: str = dc.field()
    password: str = dc.field()
    database: str = dc.field()
    max_pool_connections: int = dc.field(default=100)
    debug: bool = dc.field(default=False)
    schema: str = dc.field(default='public')


@dc.dataclass
class ProcessorPgConfig(PgConfig):
    """."""

    host: str = dc.field(default=os.getenv('PG_HOST', "localhost"))
    port: int = dc.field(default=int(os.getenv('PG_PORT', 5432)))
    user: str = dc.field(default=os.getenv('PG_USER', 'Test'))
    password: str = dc.field(default=os.getenv('PG_PASSWORD', 'Test'))
    database: str = dc.field(default=os.getenv('PG_DATABASE', 'Processor'))
