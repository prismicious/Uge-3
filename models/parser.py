import csv
import itertools
from typing import List
from models.Cereal import Cereal


class Parser():
    """" This class is responsible for reading the CSV file and returning a list of Cereal objects """
    def __init__(self, file="Cereal"):
        self.file = file
        self.file_path = f"data/{self.file}.csv"

    def read_csv(self):
        with open(self.file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            rows = list(itertools.islice(reader, 2, None))
            cereals: List[Cereal] = []
            
            for row in rows:
                for key, value in row.items():
                    if isinstance(value, str):
                        row[key] = value.strip()  # Strip leading/trailing whitespace from strings
                
                cereals.append(Cereal.from_dict(row))
            return cereals
