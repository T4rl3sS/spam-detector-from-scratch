import csv
from collections import Counter

from tokenizer import tokenize

spam_counts = Counter()
ham_counts = Counter()

with open("data/training_emails.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        words = tokenize(row["text"])
        if row["label"] == "spam":
            spam_counts.update(words)
        else:
            ham_counts.update(words)

print("TOP SPAM WORDS:", spam_counts.most_common(10))
print("TOP HAM WORDS: ", ham_counts.most_common(10))