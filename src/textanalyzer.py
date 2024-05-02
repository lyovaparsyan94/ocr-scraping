import re
from string import punctuation
from config import configs
from logs.logger import logger
from repository.file_repository import FileRepository


class TextAnalyzer:
    def __init__(self):
        self.filehandler = FileRepository()
        self.doc_pattern = configs.PATTERNS.DOCTOR_PATTERN
        self.doc_patterns = configs.PATTERNS.DOCTOR_PATTERN_LIST
        self.patient_pattern = configs.PATTERNS.PATIENT_PATTERN
        self.patient_patterns = configs.PATTERNS.PATIENT_PATTERN_LIST

    def analyze_file(self, filename, file_path):
        logger.info(f'analyzing {filename}')
        data = self.filehandler.read_json_file(file_path)
        text = ''
        for page in data:
            text += data[page]
            text = text.split('\n')
            text = ''.join(text)
        patients_list = self.use_pattern(text=text, pattern_name='patients', patterns=self.patient_patterns)
        doctors_list = self.use_pattern(text=text, pattern_name='doctors', patterns=self.doc_patterns)
        doctors_list = self.extract_clean_name(doctors_list, stopwords=configs.PATTERNS.DOCTOR_STOPWORDS,
                                               list_name='doctors names')
        self.extract_clean_name(patients_list, stopwords=configs.PATTERNS.PATIENT_STOPWORDS, list_name='patients names')

    def analyze_files(self):
        files = self.filehandler.get_files_dir(file_dir=configs.DIR_CONFIG.OUTPUT_DATA_DIR, with_abspath=True)
        counter = 1
        for filename, filepath in files.items():
            self.analyze_file(filename=filename, file_path=filepath)
            logger.info(f"scanned file {counter} / {len(files)}\n")
            counter += 1
            # break

    def extract_clean_name(self, list_of_names, stopwords, list_name=''):
        if len(list_of_names) > 0:
            logger.info(f'extracting {list_name}: {list_of_names}')
            result = []
            names = [name.strip(' ') for name in list_of_names]
            names = list(set(names))
            for name in names:
                for stopword in stopwords:
                    name = name.replace(stopword, '')
                result.append(name)
            cleaned_result = list(set(result))
            result_without_substrings = self.remove_substrings(cleaned_result)
            logger.info(f'{list_name}: {result_without_substrings}')
            return cleaned_result
        logger.info(f"in '{list_name}' not found names")

    def use_pattern(self, text, patterns: list, pattern_name: str):
        names = []
        for pattern in patterns:
            values = re.compile(pattern).findall(text)
            for value in values:
                names.append(value)
        logger.info(f'scanning text for {pattern_name}')
        names = list(set(names))
        return names

    def remove_substrings(self, names):
        unique_names = set()
        for word in names:
            is_substring = any(word in other_name for other_name in names if other_name != word)
            if not is_substring:
                unique_names.add(word)
        unique_names_list = list(unique_names)
        return unique_names_list


textanalyzer = TextAnalyzer()
textanalyzer.analyze_files()
