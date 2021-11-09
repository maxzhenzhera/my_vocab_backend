from app.core.paths import LOGGING_CONFIG_PATH
from scripts.logging_ import logger
from scripts.make_directories_for_logs import make_directories_for_logs


def main():
    logger.info('Run script for preparing project environment.')

    logger.info('Creating directories for logs...')
    make_directories_for_logs(LOGGING_CONFIG_PATH)


if __name__ == '__main__':
    main()
