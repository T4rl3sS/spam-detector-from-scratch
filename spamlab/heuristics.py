import re

URGENCY_PHRASES = ["act now", "urgent", "immediately", "last chance",
                   "verify your account", "limited time"]

SUSPICIOUS_ENDINGS = [".xyz", ".top", ".click", ".gq", ".zip"]
URL_PATTERN = r"https?://\S+|www\.\S+"


def urgency_rule(subject, body):
    text = (subject + " " + body).lower()
    hits = []
    for phrase in URGENCY_PHRASES:
        if phrase in text:
            hits.append(phrase)
    return hits


def link_rule(body):
    hits = []
    for url in re.findall(URL_PATTERN, body.lower()):
        for ending in SUSPICIOUS_ENDINGS:
            if ending in url:
                hits.append(url)
                break
    return hits


def rules_score(subject, body):
    score = 0.0
    score += 0.15 * len(urgency_rule(subject, body))
    score += 0.30 * len(link_rule(body))
    return round(min(score, 1.0), 2)


if __name__ == "__main__":
    print(urgency_rule("URGENT", "Verify your account immediately"))
    print(link_rule("Log in at http://prueba-login.top now"))
    print(rules_score("URGENT", "Verify your account immediately at http://secure-login.top"))
    print(rules_score("Lunch", "See you tomorrow"))