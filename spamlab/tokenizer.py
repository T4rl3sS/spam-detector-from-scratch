import re

STOP_WORDS = {"the", "a", "an", "and", "or", "to", "of", "in", "on",
              "for", "is", "are", "it", "this", "that", "with",
              "you", "we", "my", "your","what"}

URL_PATTERN = r"https?://\S+|www\.\S+"


def tokenize(text):
    text = text.lower()
    text = re.sub(URL_PATTERN, " urltoken ", text)
    words = re.findall(r"[a-z0-9']+", text)

    filtered = []
    for w in words:
        if w not in STOP_WORDS:
            filtered.append(w)
    words = filtered

    return words


if __name__ == "__main__":
    print(tokenize("Visit www.bank-login.top now"))