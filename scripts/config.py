from pathlib import Path


__all__ = ['LOGGING_CONFIG_PATH']


SCRIPTS_DIR = Path(__file__).parent
BASE_DIR = SCRIPTS_DIR.parent
LOGGING_CONFIG_PATH = BASE_DIR / 'app' / 'utils' / 'logging_' / 'logging_config.yaml'
