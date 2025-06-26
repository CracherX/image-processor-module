"""."""
import os
import sys


def run_mule():
    from injectors import services
    services.tasks_mule().run()


if __name__ == '__main__':
    sys.path.append(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    )
    from base_sync.base_module import setup_logging
    from base_sync import FormatDumps
    from config import config
    from injectors import connections

    setup_logging(config.logging, FormatDumps)
    connections.pg.init_db()
    run_mule()
