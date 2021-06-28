from cs50 import get_string
from string import punctuation

# request input text from the user
text = get_string("Text:")

# define variables for letters, words, sentences
l = 0
w = 0
s = 0

# for loop to count letters

# count sentences by defining a sentence end then counting the number of sentences when seeing a sentence end
seen_end = False
sentence_end = {'?', '!', '.'}
for c in text:
    if c in sentence_end:
        if not seen_end:
            seen_end = True
            s += 1
        continue
    seen_end = False


# Remove puncation to make it easier to count letters in text. Can use len(text) - " "
text = ''.join(ch for ch in text if ch not in punctuation)
for char in text:
    if char != " ":
        l += 1

# use .split() to split words of string. Then count number of words as w
words = text.split()
w = len(words)

# define big L and big S
L = (l * 100) / w
S = (s * 100) / w

# equation for coleman-liau index for readability score
index = int((0.0588 * L - 0.296 * S - 15.8) + 0.5)

# print the resulting grade level from the calculated Coleman-Liau Index using index
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
