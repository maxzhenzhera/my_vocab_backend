from pathlib import Path

import yaml

from app.core.paths import LOGGING_CONFIG_PATH
from scripts.logging_ import logger


def make_directories_for_logs(config_path: Path) -> None:
    config = yaml.safe_load(config_path.read_text('utf-8'))
    for handler_name in config['handlers']:
        if 'file' in handler_name:
            log_path = Path(config['handlers'][handler_name]['filename']).resolve()
            log_dir = log_path.parent
            log_dir.mkdir(parents=True, exist_ok=True)
            logger.info(
                f'For < {handler_name} > : logs directory by path {log_dir} has been created.'
            )


if __name__ == '__main__':
    make_directories_for_logs(LOGGING_CONFIG_PATH)
