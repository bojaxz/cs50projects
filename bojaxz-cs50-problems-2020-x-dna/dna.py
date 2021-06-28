from sys import argv
import cs50

# return error message and exit program if argv does not include the appropreiate command line arguments
if len(argv) != 3:
    print("Invalid use. python dna.py filename")
    exit(1)


# open large csv (dna)
file = open(argv[1], 'r')

# define strands and person
strands = []
person = {}

# clean , from large and enter data into dict
for index, row in enumerate(file):
    if index == 0:
        strands = [strand for strand in row.strip().split(',')][1:]
    else:
        cur_row = row.strip().split(',')
        person[cur_row[0]] = [int(x) for x in cur_row[1:]]

# open dna sequence text file
dna_sequence = open(argv[2], 'r').read()

# count max/final strands and number of strands. Reads strands in a window of strand len
# increments by len strand + len strand when a match is found to determine the longest strand
total_strands = []
for strand in strands:
    i = 0
    max_strand = -1
    cur_max = 0
    while i < len(dna_sequence):
        cur_window = dna_sequence[i:i + len(strand)]
        if cur_window == strand:
            cur_max += 1
            max_strand = max(max_strand, cur_max)
            i += len(strand)
        # resets max if strand combo is broken
        else:
            cur_max = 0
            i += 1
    # adds the max strand to the total_strands list if the stand is a max strand
    total_strands.append(max_strand)

# interate through list of names to find if max strands match. Will return name if match is found

for name, data in person.items():
    if data == total_strands:
        print(name)
        exit(0)

# else print no match
print("No Match")
