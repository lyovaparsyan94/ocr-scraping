import re

from config import configs
from logs.logger import logger
from repository.file_repository import FileRepository


class TextAnalyzer:
    def __init__(self):
        self.filehandler = FileRepository()
        self.doc_pattern0 = re.compile(r"A/PROF\s+(\w+\s+\w+)")
        self.doc_pattern1 = re.compile(r"Dr\s+(\w+\s+\w+)")
        self.doc_pattern2 = re.compile(r"Mr\s+(\w+\s+\w+)")
        self.doc_pattern3 = re.compile(r"Dr\s+[A-Za-z]+\s+[A-Za-z]+")
        self.patient_pattern3 = re.compile(r"Mr\s+[A-Za-z]+\s+[A-Za-z]+")
        self.doc_patterns = [self.doc_pattern3]
        self.patient_patterns = [re.compile(r"Mr\s+[A-Za-z]+\s+[A-Za-z]+"), re.compile(r"Mr\s+(\w+\s+\w+)")]

    def analyze_file(self, pdf):
        data = self.filehandler.read_json_file(pdf)
        text = ...
        text = text.split('\n')
        text = ''.join(text)
        self.use_pattern(text=text, pattern_name='patients', patterns=self.patient_patterns)
        self.use_pattern(text=text, pattern_name='doctors', patterns=self.doc_patterns)

    def analyze_files(self):
        files_dir = self.filehandler.get_files_dir(file_dir=configs.DIR_CONFIG.INITIAL_DATA_DIR)
        for file_dir in files_dir:
            self.analyze_file(file_dir)

    def use_pattern(self, text, patterns: list, pattern_name: str):
        names = []
        for pattern in patterns:
            values = pattern.findall(text)
            for value in values:
                names.append(value)
        logger.info(f'Found {pattern_name}\n{names}')


sc = TextAnalyzer()
sc.analyze_files()
