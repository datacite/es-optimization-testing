import csv
import random

class QueryGenerator:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.queries = []

        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                self.queries = list(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

    def get_random_query(self):
        return random.choice(self.queries)
