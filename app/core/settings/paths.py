from pathlib import Path


__alL__ = [
    'APP_DIR',
    'BASE_DIR',
    'EMAIL_TEMPLATES_DIR',
    'ALEMBIC_CONFIG_PATH',
    'LOGGING_CONFIG_PATH'
]


APP_DIR = Path(__file__).parent.parent.parent
BASE_DIR = APP_DIR.parent
EMAIL_TEMPLATES_DIR = APP_DIR / 'email_templates'

ALEMBIC_CONFIG_PATH = BASE_DIR / 'alembic.ini'
LOGGING_CONFIG_PATH = BASE_DIR / 'configs' / 'logging.yaml'
