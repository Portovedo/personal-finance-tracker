
import csv
from typing import List, Dict

class CSVParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse(self) -> List[Dict]:
        """
        Parses a CSV file and returns a list of dictionaries.
        """
        with open(self.file_path, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)
