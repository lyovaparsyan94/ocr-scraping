import math
import re
from collections import Counter

from config import configs
from logs.logger import logger
from repository.file_repository import FileRepository


class TextAnalyzer:
    def __init__(self):
        self.full_text = ''
        self.filehandler = FileRepository()
        self.doc_pattern = configs.PATTERNS.DOCTOR_PATTERN
        self.doc_patterns = configs.PATTERNS.DOCTOR_PATTERN_LIST
        self.patient_pattern = configs.PATTERNS.PATIENT_PATTERN
        self.patient_patterns = configs.PATTERNS.PATIENT_PATTERN_LIST

    def get_full_text(self, data):
        text = ''
        for page in data:
            text += data[page]
        return text

    def analyze_file(self, filename, file_path):
        data = self.filehandler.read_json_file(file_path)
        self.full_text = self.get_full_text(data)
        prepared_text = self.prepare_text()
        doctors = self.use_pattern(prepared_text, pattern_name='doctors')
        doctors_cleaned = self.extract_clean_names(names=doctors, list_name='doctors',
                                                   stopwords=configs.PATTERNS.DOCTOR_STOPWORDS)
        if doctors_cleaned:
            doctors_duplicated = self.save_duplicated_names(names=doctors_cleaned, list_name='doctors duplicated')
            logger.info(f"MAIN doctor: {max(doctors_duplicated, key=doctors_duplicated.get)}")
        else:
            logger.info("MAIN doctor NOT FOUND")

    def save_duplicated_names(self, names, list_name):
        optimised_duplicates = self.get_similar_names(names)
        full_text = self.full_text.replace('\n\n', '\n')
        duplicated_names = {}
        for name in optimised_duplicates:
            for doctor in optimised_duplicates[name]:
                if doctor in full_text:
                    if name not in duplicated_names:
                        duplicated_names[name] = full_text.lower().count(doctor.lower())
                    else:
                        duplicated_names[name] += full_text.lower().count(doctor.lower())

        logger.info(f"{list_name}: {duplicated_names}")
        return duplicated_names

    def analyze_files(self):
        files = self.filehandler.get_files_dir(file_dir=configs.DIR_CONFIG.OUTPUT_DATA_DIR, with_abspath=True)
        counter = 1
        for filename, filepath in files.items():
            logger.info(f"scanning {filename}")
            self.analyze_file(filename=filename, file_path=filepath)
            logger.info(f"scanned {counter} / {len(files)}, file: {filename}\n")
            counter += 1

    def extract_clean_names(self, names, stopwords, list_name=''):
        if len(names) > 0:
            result = []
            names = [name.strip(' ') for name in names]
            for name in names:
                for stopword in stopwords:
                    name = name.replace(stopword, '')
                result.append(name)
            result = self.extract_full_names(result)
            logger.info(f'extracted {list_name}: length {len(result)} {result}')
            return result
        logger.info(f"in '{list_name}' not found names")

    def use_pattern(self, lines, patterns: list = configs.PATTERNS.DOCTOR_PATTERN_LIST, pattern_name: str = ''):
        names = []
        for line in lines:
            for pattern in patterns:
                values = re.compile(pattern).findall(line)
                for value in values:
                    names.append(value)
            names = list(set(names))
        logger.info(f"pattern used: length - {len(names)}")
        return names

    def remove_substrings(self, names):
        unique_names = set()
        for word in names:
            is_substring = any(word in other_name for other_name in names if other_name != word)
            if not is_substring:
                unique_names.add(word)
        unique_names_list = list(unique_names)
        return unique_names_list

    def extract_full_names(self, names):
        for i in range(len(names)):
            name = names[i]
            full_name = self.extract_full_name(text_line=self.full_text.replace('\n\n', '\n'), target_name=name)
            names[i] = full_name
        return names

    def extract_full_name(self, text_line, target_name):
        target_name = target_name.strip()
        target_index = text_line.find(target_name)
        if target_index != -1:
            full_name = target_name
            for char in text_line[target_index + len(target_name):]:
                if char.isalpha():
                    full_name += char
                else:
                    break
            return full_name.strip()
        else:
            return text_line.strip()

    def prepare_text(self):
        lines = self.full_text.split('\n')
        new_lines = []
        for line in lines:
            for keyword in configs.PATTERNS.DOCTORS_KEYWORDS:
                if line.lower().count('dr') > 1:
                    doctor_segments = [f"Dr {segment.strip()}" for segment in line.split("Dr") if
                                       segment.strip()]
                    new_lines.extend(doctor_segments)
                elif keyword in line.lower():
                    new_lines.append(line)
        return new_lines

    def get_similarity_rate(self, first_name_to_compare, second_name_to_compare):
        words1 = re.findall(r'\w+', first_name_to_compare.lower())
        words2 = re.findall(r'\w+', second_name_to_compare.lower())

        vec1 = Counter(words1)
        vec2 = Counter(words2)

        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum(vec1[x] * vec2[x] for x in intersection)
        denominator1 = math.sqrt(sum(vec1[x] ** 2 for x in vec1))
        denominator2 = math.sqrt(sum(vec2[x] ** 2 for x in vec2))
        similarity_rate = numerator / (denominator1 * denominator2)

        return similarity_rate

    def get_similar_names(self, names):
        similar_names_dict = {}
        processed_names = set()
        for name1 in names:
            if name1 not in processed_names:
                similar_names_dict[name1] = []
                processed_names.add(name1)
                for name2 in names:
                    if name1 != name2 and name2 not in processed_names:
                        similarity_rate = self.get_similarity_rate(name1, name2)
                        if similarity_rate > 0.49:
                            similar_names_dict[name1].append(name2)
                            processed_names.add(name2)
                            if name1 not in similar_names_dict[name1]:
                                similar_names_dict[name1].append(name1)
        if all(not v for v in similar_names_dict.values()):
            for key, value in similar_names_dict.items():
                similar_names_dict[key] = [str(key)]
            return similar_names_dict
        similar_names_dict = {key: value for key, value in similar_names_dict.items() if value}
        resul_dict = {}
        for key in similar_names_dict:
            longest_word = max(similar_names_dict[key])
            if longest_word not in resul_dict:
                resul_dict[longest_word] = similar_names_dict[key]
        return resul_dict


textanalyzer = TextAnalyzer()
textanalyzer.analyze_files()
