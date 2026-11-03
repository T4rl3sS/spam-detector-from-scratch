import csv
import math
from collections import Counter

from tokenizer import tokenize


class NaiveBayes:
    def __init__(self):
        self.word_counts = {"spam": Counter(), "ham": Counter()}
        self.email_counts = {"spam": 0, "ham": 0}
        self.vocab = set()

    def train(self, texts, labels):
        for text, label in zip(texts, labels):
            self.email_counts[label] += 1
            for word in tokenize(text):
                self.word_counts[label][word] += 1
                self.vocab.add(word)

    def word_probability(self, word, label):
        total_words = sum(self.word_counts[label].values())
        count = self.word_counts[label][word]
        return (count + 1) / (total_words + len(self.vocab))

    def spam_probability(self, text):
        total_emails = sum(self.email_counts.values())
        log_spam = math.log(self.email_counts["spam"] / total_emails)
        log_ham = math.log(self.email_counts["ham"] / total_emails)

        for word in tokenize(text):
            if word not in self.vocab:
                continue
            log_spam += math.log(self.word_probability(word, "spam"))
            log_ham += math.log(self.word_probability(word, "ham"))

        biggest = max(log_spam, log_ham)
        spam_score = math.exp(log_spam - biggest)
        ham_score = math.exp(log_ham - biggest)
        return spam_score / (spam_score + ham_score)


if __name__ == "__main__":
    texts, labels = [], []
    with open("data/training_emails.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            texts.append(row["text"])
            labels.append(row["label"])

    model = NaiveBayes()
    model.train(texts, labels)
    print(model.email_counts)
    print(len(model.vocab))
    print(model.word_counts["spam"]["free"], model.word_counts["ham"]["free"])
    print(model.spam_probability("Claim your free prize now"))
    print(model.spam_probability("Please review the attached notes"))
    print(model.spam_probability("free"))
    print(model.spam_probability("free lunch tomorrow at the office"))
    print(model.spam_probability("meeting notes attached, click here"))
    print(model.spam_probability("zebra giraffe"))
    print(model.spam_probability("adjunto el resultado final"))
    print(model.spam_probability("hola, adjunto la agenda de manana"))
    print(model.spam_probability("gana premio gratis ahora"))
    print(model.spam_probability("el informe esta listo"))
    print(model.spam_probability("zebra giraffe lottery meeting"))
    print(model.spam_probability("lottery"))
    print(model.spam_probability("meeting"))

    tests = [
        "lottery",
        "meeting",
        "zebra giraffe lottery meeting",
        "hola, adjunto la agenda de manana",
        "gana premio gratis ahora",
        "el informe esta listo",
    ]
    for t in tests:
        print(round(model.spam_probability(t), 3), "<-", t)