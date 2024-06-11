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


class PatternConfigs(BaseSettings):
    PATIENT_PATTERN: str = r"Mr\s+(\w+\s+\w+)"
    PATIENT_PATTERN_LIST: list = [r"Mr\s+[A-Za-z]+\s+[A-Za-z]+", r"Mr\s+(\w+\s+\w+)", ]
    PATIENT_STOPWORDS: list = ['Ms ', 'Mr ', 'MR ', 'Mr', 'MR', 'Ms', 'MS', 'MS ', 'Ms. ', 'Mr. ', 'MR. ', 'Mr.', 'MR.',
                               'Ms.', 'MS.', 'MS. ', ]
    DOCTOR_PATTERN: str = r"Dr\s+(\w+\s+\w+)"
    # DOCTOR_PATTERN_LIST: list = [
    #     r"A/PROF\s+(\w+\s+\w+)",
    #     r"([A-Z][a-z]+ [A-Z][a-z]+) \(Prov",
    #     r'Dr\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:-[A-Z][a-z]+)?',
    # ]
    DOCTOR_PATTERN_LIST: list = [
        # r"Dr\s+(\w+\s+\w+)",                                    #
        r"A/PROF\s+(\w+\s+\w+)",
        r"([A-Z][a-z]+ [A-Z][a-z]+) \(Prov",
        r"Dr\s+[A-Za-z]+\s+[A-Za-z]+",
        # r'Dr\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?',
        # r'Dr\s+[A-Z][a-z]+(?:-[A-Z][a-z]+)?(?:\s+[A-Z][a-z]+)?',
        r'Dr\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:-[A-Z][a-z]+)?',
    ]
    DOCTOR_STOPWORDS: list = ['DR. ', 'Dr. ', 'Dr.', 'DR.', 'DR ', 'Dr ', 'Dr', 'DR', ]
    DOCTORS_KEYWORDS: list = ['dr', 'prof', 'prov.', ]


class Config(BaseSettings):
    DIR_CONFIG: DirConfigs = DirConfigs()
    PATTERNS: PatternConfigs = PatternConfigs()


configs = Config()
