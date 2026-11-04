import re
from urllib.parse import urlparse

URGENCY_PHRASES = ["act now", "urgent", "immediately", "last chance",
                   "verify your account", "limited time"]

SUSPICIOUS_ENDINGS = [".xyz", ".top", ".click", ".gq", ".zip"]
URL_PATTERN = r"https?://[^\s\"'<>]+|www\.[^\s\"'<>]+"
HREF_PATTERN = r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>'


def host_of(url):
    if not url.startswith("http"):
        url = "http://" + url
    return (urlparse(url).hostname or "").lower()


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
        host = host_of(url)
        for ending in SUSPICIOUS_ENDINGS:
            if host.endswith(ending):
                hits.append(host)
                break
    return hits


def mismatch_rule(body):
    hits = []
    for href, label in re.findall(HREF_PATTERN, body, re.IGNORECASE | re.DOTALL):
        shown = re.search(r"[a-z0-9-]+(\.[a-z0-9-]+)+", label.lower())
        real = host_of(href)
        if shown and real:
            shown_domain = shown.group(0).removeprefix("www.")
            if shown_domain not in real:
                hits.append(shown_domain + " -> " + real)
    return hits


def rules_score(subject, body):
    score = 0.0
    score += 0.15 * len(urgency_rule(subject, body))
    score += 0.30 * len(link_rule(body))
    score += 0.50 * len(mismatch_rule(body))
    return round(min(score, 1.0), 2)


if __name__ == "__main__":
    print(urgency_rule("URGENT", "Verify your account immediately"))
    print(link_rule("Log in at http://secure-login.top now"))
    print(link_rule("Read http://desktop.topics.com/news"))
    print(mismatch_rule('<a href="http://198.51.100.7/login">www.mybank.com</a>'))
    print(mismatch_rule('<a href="https://mybank.com/login">www.mybank.com</a>'))
    print(rules_score("Verify your account", 'Act now: <a href="http://198.51.100.7/login">www.mybank.com</a>'))
    print(rules_score("Lunch", "See you tomorrow"))
    print(rules_score("Break", "See you monday"))