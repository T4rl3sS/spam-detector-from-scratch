# spam-detector-from-scratch

A small spam detector that I built **step by step, from scratch**, to learn how spam filters really work inside. No machine learning libraries, only plain Python.

## Why I built this

Everyone talks about "AI detects spam", but almost nobody shows how it works. I'm learning, so I built the pieces one at a time, and each commit in this repo is one step.

## How it works

A real spam filter is not one model. It is several layers whose scores are combined:

```
email ──▶  1. Authentication  (SPF / DKIM / DMARC)   auth.py
      ──▶  2. Content model   (Naive Bayes)          naive_bayes.py
      ──▶  3. Rules           (urgency, bad links)   heuristics.py
                     │
                     ▼
         4. Combine the scores                       detector.py
                     │
                     ▼
         INBOX  /  SPAM FOLDER  /  REJECT
```

## Project structure

```
spamlab/
  tokenizer.py     text -> list of words
  counting.py      count words in spam vs. normal email
  naive_bayes.py   the content model (training + prediction)
  heuristics.py    rule-based checks and a rules score
  auth.py          sender authentication score
  detector.py      combines everything into one decision
data/
  training_emails.csv
```

## Run it

```bash
git clone https://github.com/T4rl3sS/spam-detector-from-scratch.git
cd spam-detector-from-scratch
python3 spamlab/detector.py
```

Sample output:

```
Normal work email
  content: 0.0  rules: 0.0  auth: 0.0
  FINAL: 0.0 -> INBOX
Prize scam
  content: 1.0  rules: 0.45  auth: 0.85
  FINAL: 0.797 -> SPAM FOLDER
Phishing with fake link
  content: 1.0  rules: 0.8  auth: 0.9
  FINAL: 0.913 -> REJECT
Legit newsletter, sloppy sender setup
  content: 0.06  rules: 0.0  auth: 0.33
  FINAL: 0.109 -> INBOX
```

Each file can also be run on its own (`python3 spamlab/tokenizer.py`, `python3 spamlab/auth.py`, ...) to see that layer working alone.

## The layers

**1. Tokenizer.** The computer can't read text, only count things. The tokenizer lowercases the text, removes punctuation, drops filler words ("the", "and"), and replaces every link with one marker word (`urltoken`), so the model learns "has a link" without memorizing each link.

**2. Naive Bayes.** Training means counting how often each word appears in spam vs. normal email ("ham"). To predict, it multiplies the word probabilities with Bayes' rule. Three details that matter:
- It adds **logarithms** instead of multiplying, because hundreds of tiny numbers would round down to zero.
- **Smoothing (+1)** stops a word never seen in one class (like `free` in ham) from making the whole probability zero.
- Words the model has never seen are **skipped**.

**3. Rules.** Hand-written checks for things word counts can't see: urgency phrases ("verify your account"), links that end in suspicious domains (`.top`, `.xyz`), and the classic phishing trick where the link **text** shows `mybank.com` but the **real** destination is somewhere else.

**4. Authentication.** Before reading any text, a mail server checks who is sending: **SPF** (is this server allowed to send for the domain?), **DKIM** (is the message signed and unchanged?) and **DMARC** (do those checks match the visible From address?). The results become a risk score.

**5. Combining.** A weighted average (content 45%, rules 30%, authentication 25%) and two thresholds decide what happens to the email.

## What I learned (the bugs I found)

- **A false positive from one word.** My model scored the normal Spanish email "adjunto el resultado final" as **66% spam**. It had only seen English, so three of the four words were unknown and skipped, and the one it knew (`final`) only appeared in a spam email. After adding a few Spanish examples to the training data, the score dropped to **7.6%**.
- **Testing on training data proves little.** My fix used a sentence almost identical to the test, so I wrote new test sentences the model had never seen.
- **Words can cancel out.** `zebra giraffe lottery meeting` scored 49%: `lottery` pushes toward spam, `meeting` pushes toward ham, and the unknown words are ignored.
- **A sloppy rule gives false alarms.** My first link rule used `".top" in url`, which would flag the harmless `desktop.topics.com`. I changed it to check how the **domain** ends.
- **No single layer decides.** A legitimate newsletter with a sloppy sender setup still reaches the inbox, because the text and rules look fine.

## Limitations

- The model trains on only 35 short emails, so its numbers are shaky. Real filters train on millions.
- The tokenizer only understands plain English letters, so accented characters (`ñ`, `é`) split words apart.
- The rules and weights are chosen by hand. Real systems learn them from data.
- It works on the text I give it. It doesn't read real email files or check real servers.

## What real systems add

Transformer models that understand context, sender reputation and blocklists, learning from millions of "Report spam" clicks, and constant retraining as spammers adapt.

## Ideas for next steps

- Handle accents in the tokenizer (`[\w']+`).
- Add many more training emails and measure accuracy on emails the model never saw.
- Learn the layer weights from data instead of choosing them by hand.
- Compare with a library model (for example scikit-learn).

## About

An educational project. Use it however you like.
