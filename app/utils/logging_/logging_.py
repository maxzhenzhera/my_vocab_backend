import pathlib

import yaml


__all__ = ['get_logging_config']


def get_logging_config(config_path: pathlib.Path) -> dict:
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file.read())

    _create_dirs_for_logs(config)

    return config


def _create_dirs_for_logs(config: dict) -> None:
    for handler_name in config['handlers']:
        if 'file' in handler_name:
            log_path = pathlib.Path(config['handlers'][handler_name]['filename'])
            log_dir_path = log_path.parent
            log_dir_path.mkdir(parents=True, exist_ok=True)
