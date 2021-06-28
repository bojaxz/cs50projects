# TODO
import cs50
from sys import argv

# check command-line length
if len(argv) != 2:
    print('Usage: python roster.py name of house')
    exit(1)

# open database then execute select statement
db = cs50.SQL("sqlite:///students.db")
rows = db.execute('SELECT * FROM students WHERE house = ? ORDER BY last, first', argv[-1])

# print query results
for row in rows:
    print(row['first'] + ' ' + (row['middle'] + ' ' if row['middle'] else '') + row['last'] + ', born ' + str(row['birth']))