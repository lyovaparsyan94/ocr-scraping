import time
from os.path import join

import gevent
from logs.logger import logger
from pdf2image import convert_from_path
from pytesseract import pytesseract
from repository.file_repository import FileRepository

from src.config import configs


class PDFScannerUseCase:
    def __init__(self):
        self.filehandler = FileRepository()

    def scan_pdf(self, pdf_file: str, pdf_name: str) -> None:
        """
        Scans a PDF file and extracts text from each page.

        Args:
            pdf_file (str): Path to the input PDF file.
            pdf_name (str): Name of the PDF.

        Returns:
            None: Saves the extracted text to a JSON file.
        """
        pdf_data = {pdf_name: {}}
        pages = convert_from_path(pdf_file, 500)
        json_filename = join(configs.DIR_CONFIG.OUTPUT_DATA_DIR, f'{pdf_name[:-4]}.json')
        for page_num, imgblob in enumerate(pages, start=1):
            scanned_text = pytesseract.image_to_string(imgblob, lang='eng')
            pdf_data[pdf_name][str(page_num)] = scanned_text
            logger.info(f' - processing page {page_num} / {len(pages)}')
            txt_filename = join(configs.DIR_CONFIG.OUTPUT_DATA_DIR, f'{pdf_name[:-4]}{page_num}.txt')
            self.filehandler.create_file(filename=txt_filename, text=scanned_text)
        self.filehandler.save_data(filename=json_filename, data=pdf_data)

    def scan_all_pdfs(self) -> None:
        """
        Scans all PDF files in the specified directory.

        Returns:
            None: Saves extracted text for all PDFs.
        """
        start = time.time()
        pdfs = self.filehandler.get_files_dir()
        for counter, pdf in enumerate(pdfs, start=1):
            logger.info(f'scanning {counter} / {len(pdfs)} files: current - {pdf}')
            if pdf.lower().endswith('.pdf'):
                pdf_name = pdf
                pdf = join(configs.DIR_CONFIG.INITIAL_DATA_DIR, pdf)
                self.scan_pdf(pdf_file=pdf, pdf_name=pdf_name)
        end = time.time()
        logger.info(f'Done in {end - start} secs')

    def scan_all_pdfs_gevent(self) -> None:
        start = time.time()
        pdfs = self.filehandler.get_files_dir()
        jobs = [gevent.spawn(self.scan_pdf, join(configs.DIR_CONFIG.INITIAL_DATA_DIR, pdf), pdf) for pdf in pdfs if
                pdf.lower().endswith('.pdf')]
        gevent.joinall(jobs)
        end = time.time()
        logger.info(f'GEVENT: Done in {end - start} secs')


pdf_scanner = PDFScannerUseCase()
pdf_scanner.scan_all_pdfs()
# pdf_scanner.scan_all_pdfs_gevent()
