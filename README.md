# spam-detector-from-scratch

A spam detector built from scratch in plain Python, with no machine learning libraries. The goal is to show how a spam filter works internally, one layer at a time.

## Overview

The detector reads an email and returns one of three decisions: **inbox**, **spam folder** or **reject**. The decision combines three independent checks:

| Check | What it does |

| Content | A Naive Bayes classifier scores how much the text looks like spam, based on word frequencies in the training data. |
| Rules | Simple rules flag urgent phrases, suspicious domains, and links whose visible text does not match their real destination. |
| Sender | A score derived from the SPF, DKIM and DMARC results, which mail servers use to verify who sent a message. |

Each check produces a score between 0 and 1. A weighted average of the three scores gives the final decision.

## Project structure

```
spamlab/
  tokenizer.py     converts text into a list of words
  counting.py      counts words in spam and normal email
  naive_bayes.py   content classifier (training and prediction)
  heuristics.py    rule-based checks
  auth.py          sender authentication score
  detector.py      combines all scores into a decision
data/
  training_emails.csv
```

## Usage

Requires Python 3.9 or later.

```bash
git clone https://github.com/T4rl3sS/spam-detector-from-scratch.git
cd spam-detector-from-scratch
python3 spamlab/detector.py
```

Each module can also be run on its own to inspect a single layer, for example `python3 spamlab/auth.py`.

## Notes

- The classifier trains on a small set of 35 example emails, so its scores are only illustrative. A model trained on this little data can be misled by a single word. In testing, a normal Spanish email scored 66% spam until Spanish examples were added to the training data, after which it scored 7.6%.
- The tokenizer handles plain English letters only.
- Rule lists and score weights are set by hand.

## License

Educational project. Free to use and modify.
