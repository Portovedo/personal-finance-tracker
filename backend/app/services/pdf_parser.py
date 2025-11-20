
import pdfplumber
from typing import List

class PDFParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_text(self) -> List[str]:
        """
        Extracts text from a PDF file.
        """
        with pdfplumber.open(self.file_path) as pdf:
            text = []
            for page in pdf.pages:
                text.extend(page.extract_text().split('\n'))
        return text
