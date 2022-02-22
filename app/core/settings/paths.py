from pathlib import Path


__alL__ = [
    'APP_DIR',
    'BASE_DIR',
    'LOGGING_CONFIG_PATH',
    'EMAIL_TEMPLATES_DIR'
]


APP_DIR = Path(__file__).parent.parent
BASE_DIR = APP_DIR.parent
LOGGING_CONFIG_PATH = APP_DIR / 'utils' / 'logging_' / 'logging_config.yaml'
EMAIL_TEMPLATES_DIR = APP_DIR / 'email_templates'
