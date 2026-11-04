import re

RISK = {"pass": 0.0, "neutral": 0.4, "none": 0.5, "softfail": 0.6, "fail": 1.0}
WEIGHTS = {"dmarc": 0.45, "dkim": 0.30, "spf": 0.25}


def parse_auth(header):
    results = {}
    for method in WEIGHTS:
        match = re.search(method + r"\s*=\s*(\w+)", header.lower())
        if match:
            results[method] = match.group(1)
        else:
            results[method] = "none"
    return results


def auth_score(header):
    results = parse_auth(header)
    score = 0.0
    for method, outcome in results.items():
        score += WEIGHTS[method] * RISK.get(outcome, 0.5)
    return round(score, 2)


if __name__ == "__main__":
    print(parse_auth("spf=pass dkim=fail dmarc=fail"))
    print(auth_score("spf=pass dkim=pass dmarc=pass"))
    print(auth_score("spf=fail dkim=fail dmarc=fail"))
    print(auth_score("spf=softfail dkim=none dmarc=fail"))
    print(auth_score(""))