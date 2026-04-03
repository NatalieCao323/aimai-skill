"""
bayesian_tagger.py

Bayesian signal tagger for crush.skill.

Each interaction fragment is scored across three dimensions:
  - prior_confidence   P(H): estimated probability that the message reflects genuine intent
  - time_decay         lambda: rate at which the signal fades over time
  - emotional_intensity E: valence and arousal of the interaction (-1.0 to +1.0)

Progression weight formula:
  W_t = P(H) * exp(-lambda * delta_t) * (1 + E)

Where delta_t is the number of days since the interaction occurred.

Usage:
  python3 bayesian_tagger.py --text "message text" --days 7
  python3 bayesian_tagger.py --file chat_parsed.txt
  python3 bayesian_tagger.py --file chat_parsed.txt --summary
"""

import argparse
import json
import math
import re
import sys


# ---------------------------------------------------------------------------
# Signal classification rules
# ---------------------------------------------------------------------------

REJECTION_SIGNALS = [
    "不想谈恋爱", "只当朋友", "没感觉", "不合适", "不喜欢你",
    "just friends", "not interested", "i don't like you that way",
]

AVOIDANCE_SIGNALS = [
    "改天", "有空再说", "最近很忙", "再说吧", "以后再聊",
    "maybe later", "i'm busy", "let's see",
]

POSITIVE_SIGNALS = [
    "要是你在就好了", "想你了", "吃醋", "好想见你", "只有你",
    "miss you", "wish you were here", "thinking of you",
]

AMBIGUOUS_SIGNALS = [
    "哈哈", "随便", "无所谓", "都行", "你说呢",
    "haha", "whatever", "up to you",
]


def classify_prior_confidence(text: str) -> float:
    """
    Estimate P(H): probability that the message reflects genuine intent.

    Returns a value in [0.0, 1.0]. High-confidence rejection signals return
    values near 0.9 (the rejection is likely real). Positive signals return
    moderate-to-high confidence. Ambiguous filler returns low confidence.
    """
    text_lower = text.lower()

    for phrase in REJECTION_SIGNALS:
        if phrase in text_lower:
            return 0.9

    for phrase in POSITIVE_SIGNALS:
        if phrase in text_lower:
            return 0.7

    for phrase in AVOIDANCE_SIGNALS:
        if phrase in text_lower:
            return 0.2

    for phrase in AMBIGUOUS_SIGNALS:
        if phrase in text_lower:
            return 0.15

    return 0.4


def classify_time_decay(text: str) -> float:
    """
    Estimate lambda: the decay rate for this type of interaction.

    Emotionally significant exchanges decay slowly (low lambda).
    Routine check-ins and filler messages decay quickly (high lambda).
    """
    text_lower = text.lower()

    for phrase in POSITIVE_SIGNALS + REJECTION_SIGNALS:
        if phrase in text_lower:
            return 0.1

    if len(text) > 80:
        return 0.2

    for phrase in AVOIDANCE_SIGNALS:
        if phrase in text_lower:
            return 0.5

    return 0.9


def classify_emotional_intensity(text: str) -> float:
    """
    Estimate E: emotional valence and intensity of the interaction.

    Range: -1.0 (strong negative) to +1.0 (strong positive).
    """
    text_lower = text.lower()

    for phrase in REJECTION_SIGNALS:
        if phrase in text_lower:
            return -0.8

    for phrase in POSITIVE_SIGNALS:
        if phrase in text_lower:
            return 0.8

    for phrase in AVOIDANCE_SIGNALS:
        if phrase in text_lower:
            return -0.3

    for phrase in AMBIGUOUS_SIGNALS:
        if phrase in text_lower:
            return 0.0

    return 0.1


def compute_progression_weight(prior: float, decay: float,
                                emotion: float, days: int) -> float:
    """
    W_t = P(H) * exp(-lambda * delta_t) * (1 + E)
    """
    return prior * math.exp(-decay * days) * (1 + emotion)


def tag_interaction(text: str, days: int = 0) -> dict:
    """Tag a single interaction fragment and return a structured result."""
    prior = classify_prior_confidence(text)
    decay = classify_time_decay(text)
    emotion = classify_emotional_intensity(text)
    weight = compute_progression_weight(prior, decay, emotion, days)

    return {
        "interaction_fragment": text,
        "tags": {
            "prior_confidence": round(prior, 4),
            "time_decay": round(decay, 4),
            "emotional_intensity": round(emotion, 4),
        },
        "progression_weight": round(weight, 4),
        "days_passed": days,
    }


def tag_file(filepath: str) -> list:
    """
    Read a parsed chat file and tag each line.
    Expected format per line: "SENDER: message text"
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
    except FileNotFoundError:
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    results = []
    for i, line in enumerate(lines):
        text = line.split(": ", 1)[1] if ": " in line else line
        result = tag_interaction(text, days=max(0, len(lines) - i))
        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Bayesian signal tagger for crush.skill"
    )
    parser.add_argument("--text", type=str, help="Single message text to tag")
    parser.add_argument("--days", type=int, default=0,
                        help="Days since the interaction (default: 0)")
    parser.add_argument("--file", type=str,
                        help="Path to a parsed chat file (one message per line)")
    parser.add_argument("--summary", action="store_true",
                        help="Print aggregate summary instead of per-message output")

    args = parser.parse_args()

    if args.text:
        result = tag_interaction(args.text, args.days)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.file:
        results = tag_file(args.file)

        if args.summary:
            if not results:
                print("No messages to analyze.")
                return
            avg_weight = sum(r["progression_weight"] for r in results) / len(results)
            max_r = max(results, key=lambda r: r["progression_weight"])
            min_r = min(results, key=lambda r: r["progression_weight"])
            print(json.dumps({
                "total_messages": len(results),
                "average_progression_weight": round(avg_weight, 4),
                "strongest_signal": max_r,
                "weakest_signal": min_r,
            }, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(results, ensure_ascii=False, indent=2))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
