import os
from os.path import join

from pydantic_settings import BaseSettings

BASE_DIR = os.path.abspath(__file__)
project_dir = os.path.dirname(os.path.dirname(BASE_DIR))
ENV_DIR = join(project_dir, '.env')


class DirConfigs(BaseSettings):
    SRC_DIR: str = os.path.dirname(BASE_DIR)
    DATA_DIR: str = join(SRC_DIR, join('data'))
    INITIAL_DATA_DIR: str = join(DATA_DIR, join('initial_data'))
    OUTPUT_DATA_DIR: str = join(DATA_DIR, join('output_data'))
    LOGS_DIR: str = join(SRC_DIR, join('logs'))
    LOG_FILE: str = join(LOGS_DIR, 'logs.log')
    LOG_CONFIG_FILE: str = join(LOGS_DIR, 'logging.yaml')


class Config(BaseSettings):
    DIR_CONFIG: DirConfigs = DirConfigs()


configs = Config()
