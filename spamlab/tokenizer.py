import re

STOP_WORDS = {"the", "a", "an", "and", "or", "to", "of", "in", "on",
              "for", "is", "are", "it", "this", "that", "with",
              "you", "we", "my", "your"}


def tokenize(text):
    text = text.lower()
    words = re.findall(r"[a-z0-9']+", text)

    filtered = []
    for w in words:
        if w not in STOP_WORDS:
            filtered.append(w)
    words = filtered

    return words


print(tokenize("Click the link and win a prize"))