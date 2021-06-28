import cs50
import csv
from sys import argv

if len(argv) != 2:
    print('Usage: python import.py file_name.csv')
    exit(1)

db = cs50.SQL("sqlite:///students.db")

# Create tables

# Open TSV file
with open(argv[-1], "r") as characters:

    # Create DictReader
    reader = csv.DictReader(characters)

    # Iterate over TSV file
    for row in reader:

        current_name = row['name'].split()
        first = current_name[0]
        middle = current_name[1] if len(current_name) == 3 else None
        last = current_name[-1]
        house = row['house']
        birth = row['birth']

        # Insert show
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", first, middle, last, house, birth)

print("finished")
