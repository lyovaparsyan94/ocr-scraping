import os
from os.path import join

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
        filename = join(configs.DIR_CONFIG.OUTPUT_DATA_DIR, f'{pdf_name[:-4]}.json')
        for page_num, imgblob in enumerate(pages, start=1):
            scanned_text = pytesseract.image_to_string(imgblob, lang='eng')
            pdf_data[pdf_name][str(page_num)] = scanned_text
            print(f' - processing page {page_num} / {len(pages)}')
        self.filehandler.save_data(data=pdf_data, filename=filename)

    def scan_all_pdfs(self) -> None:
        """
        Scans all PDF files in the specified directory.

        Returns:
            None: Saves extracted text for all PDFs.
        """
        pdfs = self.get_pdfs_dir()
        count_of_files = len(pdfs)
        print(f"get total {count_of_files} files ")
        for counter, pdf in enumerate(pdfs, start=1):
            print(f'converting  {counter} / {len(pdfs)} file: {pdf}')
            if pdf.lower().endswith('.pdf'):
                pdf_name = pdf
                pdf = join(configs.DIR_CONFIG.INITIAL_DATA_DIR, pdf)
                self.scan_pdf(pdf_file=pdf, pdf_name=pdf_name)

    def get_pdfs_dir(self, pdfs_dir: str = configs.DIR_CONFIG.INITIAL_DATA_DIR, abspath: bool = False) -> list[str]:
        """
        Retrieves a list of all PDF files in the specified directory.

        Args:
            pdfs_dir (str, optional): Directory containing PDF files. Defaults to INITIAL_DATA_DIR.
            abspath (bool, optional): Return absolute paths. Defaults to False.

        Returns:
            List[str]: List of PDF filenames.
        """
        pdfs = os.listdir(pdfs_dir)
        if abspath:
            pdfs_with_abspath = [join(configs.DIR_CONFIG.INITIAL_DATA_DIR, pdf) for pdf in pdfs]
            return pdfs_with_abspath
        return pdfs


pdf_scanner = PDFScannerUseCase()
pdf_scanner.scan_all_pdfs()
