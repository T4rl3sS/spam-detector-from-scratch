import csv

from naive_bayes import NaiveBayes
from heuristics import rules_score
from auth import auth_score

WEIGHTS = {"content": 0.45, "rules": 0.30, "auth": 0.25}
SPAM_THRESHOLD = 0.60
REJECT_THRESHOLD = 0.85
TEST = 0.0009


def load_model():
    texts, labels = [], []
    with open("data/training_emails.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            texts.append(row["text"])
            labels.append(row["label"])
    model = NaiveBayes()
    model.train(texts, labels)
    return model


def analyze(model, subject, body, auth_header):
    content = model.spam_probability(subject + " " + body)
    rules = rules_score(subject, body)
    auth = auth_score(auth_header)

    final = (WEIGHTS["content"] * content
             + WEIGHTS["rules"] * rules
             + WEIGHTS["auth"] * auth)

    if final >= REJECT_THRESHOLD:
        decision = "REJECT"
    elif final >= SPAM_THRESHOLD:
        decision = "SPAM FOLDER"
    else:
        decision = "INBOX"

    return final, decision, content, rules, auth


EXAMPLES = [
    ("Normal work email",
     "Project review",
     "Attached are the notes from our review. Please send feedback by Friday.",
     "spf=pass dkim=pass dmarc=pass"),
    ("Prize scam",
     "YOU ARE A WINNER",
     "Claim your free gift card now, limited time http://free-prize.xyz",
     "spf=fail dkim=none dmarc=fail"),
    ("Phishing with fake link",
     "Verify your account",
     'Act now: <a href="http://198.51.100.7/login">www.mybank.com</a>',
     "spf=softfail dkim=fail dmarc=fail"),
    ("Legit newsletter, sloppy sender setup",
     "Our October update",
     "Here is what the team shipped this month. Thanks for reading.",
     "spf=neutral dkim=pass dmarc=none"),
]


if __name__ == "__main__":
    model = load_model()
    for name, subject, body, header in EXAMPLES:
        final, decision, content, rules, auth = analyze(model, subject, body, header)
        print(name)
        print("  content:", round(content, 2), " rules:", rules, " auth:", auth)
        print("  FINAL:", round(final, 3), "->", decision)