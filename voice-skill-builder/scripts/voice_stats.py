#!/usr/bin/env python3
"""Measure the writing habits in a folder of one person's messages.

Usage:
    python voice_stats.py <folder> [--label work] [--json out.json]

The folder holds one message per file (.txt or .md), already cleaned down to
the words the person typed (no quoted replies, no legal footers).

Prints a readable summary, and writes the full numbers as JSON if --json is
given. Standard library only.
"""
import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’-]*")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+|\n+")
CONTRACTION = re.compile(
    r"\b\w+(?:n['’]t|['’](?:s|re|ve|ll|d|m))\b", re.I
)
# Expanded forms a writer could have contracted. Rough, but consistent across
# corpora, which is what matters for comparing a draft to a profile.
EXPANDED = re.compile(
    r"\b(?:do not|does not|did not|is not|are not|was not|were not|cannot|"
    r"can not|will not|would not|should not|could not|have not|has not|"
    r"had not|i am|i will|i have|i would|you are|you will|you have|we are|"
    r"we will|we have|they are|they will|they have|it is|that is|there is|"
    r"let us)\b",
    re.I,
)
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]"
)
BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+\S", re.M)
GREETING = re.compile(
    r"^(hi|hey|hello|dear|good (?:morning|afternoon|evening)|morning|"
    r"afternoon|thanks|thank you|team|all|folks)\b",
    re.I,
)
CASUAL = [
    "yeah", "yep", "yup", "ya", "nope", "nah", "gonna", "wanna", "gotta",
    "kinda", "sorta", "lol", "haha", "lmk", "fyi", "btw", "imo", "tbh",
    "thx", "tho", "y'all", "ok", "okay", "cool", "awesome", "ugh", "hmm",
]


def pct(n, d):
    return round(100.0 * n / d, 1) if d else 0.0


def per_k(n, words):
    return round(1000.0 * n / words, 2) if words else 0.0


def quantiles(values):
    if not values:
        return {}
    s = sorted(values)

    def q(p):
        return s[min(len(s) - 1, int(round(p * (len(s) - 1))))]

    return {
        "p25": q(0.25),
        "median": statistics.median(s),
        "p75": q(0.75),
        "p90": q(0.90),
        "max": s[-1],
    }


def first_line(text):
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def last_line(text):
    for line in reversed(text.splitlines()):
        if line.strip():
            return line.strip()
    return ""


def classify_greeting(line):
    """Bucket the opening line. A greeting is a short first line or clause."""
    head = re.split(r"[,!.\n:]", line, maxsplit=1)[0].strip()
    if len(head.split()) > 4:
        return "none"
    m = GREETING.match(head)
    if m:
        word = m.group(1).lower()
        rest = head[m.end():].strip()
        return f"{word} <name>" if rest else word
    # A bare name followed by a comma or dash ("Sam," / "Sam -")
    if re.match(r"^[A-Z][a-z]+(?: [A-Z][a-z]+)?\s*[,–—-]", line):
        return "<name>,"
    return "none"


def analyze(texts):
    n = len(texts)
    all_text = "\n".join(texts)
    total_words = len(WORD.findall(all_text))

    msg_words = [len(WORD.findall(t)) for t in texts]
    sent_lens = []
    for t in texts:
        for s in SENTENCE_END.split(t):
            w = len(WORD.findall(s))
            # Skip one- and two-word fragments (greetings, sign-offs, names)
            # so they do not drag the sentence median down.
            if w >= 3:
                sent_lens.append(w)
    para_counts = [
        len([p for p in re.split(r"\n\s*\n", t) if p.strip()]) for t in texts
    ]

    contractions = len(CONTRACTION.findall(all_text))
    expanded = len(EXPANDED.findall(all_text))

    greetings = Counter(classify_greeting(first_line(t)) for t in texts)
    closers = Counter()
    for t in texts:
        lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        # The last short line is a sign-off or a typed name. If the line
        # above it is a short line ending in a comma ("Thanks,"), count
        # that one too, since that is the sign-off proper.
        tail = lines[-1]
        if len(tail.split()) <= 3:
            closers[re.sub(r"[\s,!.]+$", "", tail).lower()] += 1
            prev = lines[-2]
            if len(lines) > 2 and prev.endswith(",") and len(prev.split()) <= 3:
                closers[re.sub(r"[\s,!.]+$", "", prev).lower()] += 1

    lower = all_text.lower()
    casual = {}
    for w in CASUAL:
        pat = re.compile(r"(?<![\w'])" + re.escape(w) + r"(?![\w'])")
        hits = sum(1 for t in texts if pat.search(t.lower()))
        if hits:
            casual[w] = {"messages": hits, "pct_of_messages": pct(hits, n)}

    caps_words = re.findall(r"\b[A-Z]{3,}\b", all_text)

    def share(pred):
        return pct(sum(1 for t in texts if pred(t)), n)

    return {
        "messages": n,
        "total_words": total_words,
        "length_words": {
            **quantiles(msg_words),
            "pct_10_words_or_fewer": pct(sum(1 for w in msg_words if w <= 10), n),
            "pct_over_100_words": pct(sum(1 for w in msg_words if w > 100), n),
        },
        "sentence_words": quantiles(sent_lens),
        "paragraphs_per_message": quantiles(para_counts),
        "per_1000_words": {
            "em_dash": per_k(all_text.count("—"), total_words),
            "en_dash": per_k(all_text.count("–"), total_words),
            "spaced_hyphen": per_k(len(re.findall(r"(?<=\S) - (?=\S)", all_text)), total_words),
            "double_hyphen": per_k(all_text.count("--"), total_words),
            "semicolon": per_k(all_text.count(";"), total_words),
            "colon": per_k(len(re.findall(r":(?!//)", all_text)), total_words),
            "ellipsis": per_k(
                len(re.findall(r"\.{3}|…", all_text)), total_words
            ),
            "parenthetical": per_k(all_text.count("("), total_words),
            "exclamation": per_k(all_text.count("!"), total_words),
            "question": per_k(all_text.count("?"), total_words),
            "contraction": per_k(contractions, total_words),
            "all_caps_word": per_k(len(caps_words), total_words),
        },
        "contraction_rate_pct": pct(contractions, contractions + expanded),
        "pct_of_messages": {
            "with_exclamation": share(lambda t: "!" in t),
            "with_question": share(lambda t: "?" in t),
            "with_emoji": share(lambda t: bool(EMOJI.search(t))),
            "with_bullets": share(lambda t: bool(BULLET.search(t))),
            "with_link": share(lambda t: "http" in t),
            "starts_lowercase": share(
                lambda t: first_line(t)[:1].islower()
            ),
            # Only judged where the last line is a real sentence, not a
            # sign-off or typed name.
            "ends_without_punctuation": share(
                lambda t: len(last_line(t).split()) > 3
                and last_line(t)[-1:].isalnum()
            ),
        },
        "apostrophes": {
            "straight": all_text.count("'"),
            "curly": all_text.count("’"),
        },
        "greetings_pct": {k: pct(v, n) for k, v in greetings.most_common(8)},
        "closers_pct": {k: pct(v, n) for k, v in closers.most_common(10)},
        "casual_words": dict(
            sorted(casual.items(), key=lambda kv: -kv[1]["messages"])
        ),
        "top_caps_words": [w for w, _ in Counter(caps_words).most_common(10)],
        "hashtags_per_message": round(len(re.findall(r"(?<!\w)#\w+", lower)) / n, 2)
        if n
        else 0,
    }


def summarize(label, s):
    L, P, M = s["length_words"], s["per_1000_words"], s["pct_of_messages"]
    lines = [
        f"== {label}: {s['messages']} messages, {s['total_words']} words ==",
        f"Length: median {L.get('median')} words (p25 {L.get('p25')}, "
        f"p75 {L.get('p75')}, p90 {L.get('p90')}); "
        f"{L['pct_10_words_or_fewer']}% are 10 words or fewer",
        f"Sentences: median {s['sentence_words'].get('median')} words",
        f"Dashes per 1,000 words: em {P['em_dash']}, en {P['en_dash']}, "
        f"spaced hyphen {P['spaced_hyphen']}, double hyphen {P['double_hyphen']}",
        f"Per 1,000 words: semicolons {P['semicolon']}, colons {P['colon']}, "
        f"ellipses {P['ellipsis']}, parentheses {P['parenthetical']}, "
        f"exclamations {P['exclamation']}",
        f"Contractions: {P['contraction']} per 1,000 words; contracts "
        f"{s['contraction_rate_pct']}% of the time it could",
        f"Messages with: exclamation {M['with_exclamation']}%, question "
        f"{M['with_question']}%, emoji {M['with_emoji']}%, bullets "
        f"{M['with_bullets']}%",
        f"Starts lowercase {M['starts_lowercase']}%; ends with no punctuation "
        f"{M['ends_without_punctuation']}%",
        "Greetings: "
        + ", ".join(f"{k} {v}%" for k, v in s["greetings_pct"].items()),
        "Closers: "
        + (", ".join(f"{k} {v}%" for k, v in s["closers_pct"].items()) or "none found"),
        "Casual words (% of messages): "
        + (
            ", ".join(
                f"{k} {v['pct_of_messages']}%"
                for k, v in list(s["casual_words"].items())[:12]
            )
            or "none found"
        ),
    ]
    if s["messages"] < 50:
        lines.append(
            "NOTE: under 50 messages. Treat every number here as a rough guide."
        )
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("folder")
    ap.add_argument("--label", default=None)
    ap.add_argument("--json", dest="json_out", default=None)
    args = ap.parse_args()

    folder = Path(args.folder)
    files = sorted(
        p for p in folder.rglob("*") if p.suffix.lower() in (".txt", ".md")
    )
    texts = []
    for p in files:
        t = p.read_text(encoding="utf-8", errors="replace").strip()
        if t:
            texts.append(t)
    if not texts:
        sys.exit(f"No .txt or .md messages found in {folder}")

    stats = analyze(texts)
    label = args.label or folder.name
    print(summarize(label, stats))
    if args.json_out:
        Path(args.json_out).write_text(json.dumps({label: stats}, indent=2))
        print(f"\nFull numbers written to {args.json_out}")


if __name__ == "__main__":
    main()
