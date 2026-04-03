"""
wechat_parser.py

Chat log parser for crush.skill.

Supports the following export formats:
  - WeChatMsg txt export: timestamp + sender + content (separate lines)
  - Bracket txt format:   [YYYY-MM-DD HH:MM] sender: content
  - Liuhen JSON export:   standard JSON array from the Liuhen macOS app
  - Plaintext:            "sender: content" per line, or raw pasted text

Usage:
  python3 wechat_parser.py --file <path> --target <name> --output <output_path>
  python3 wechat_parser.py --file <path> --target <name> --output <output_path> --format auto
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Format detection
# ---------------------------------------------------------------------------

def detect_format(file_path: str) -> str:
    """Infer the file format from extension and content sample."""
    ext = Path(file_path).suffix.lower()

    if ext == ".json":
        return "liuhen"
    if ext in (".db", ".sqlite"):
        return "pywxdump"

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            sample = f.read(3000)
    except Exception:
        return "plaintext"

    # WeChatMsg standard export: "2024-01-15 22:30:01 SenderName"
    if re.search(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s+\S", sample):
        return "wechatmsg_txt"

    # Bracket format: "[2024-01-15 22:30] sender: content"
    if re.search(r"\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\]", sample):
        return "bracket_txt"

    return "plaintext"


# ---------------------------------------------------------------------------
# Format-specific parsers
# ---------------------------------------------------------------------------

def parse_wechatmsg_txt(file_path: str, target_name: str) -> dict:
    """
    Parse WeChatMsg txt export.
    Line format: "2024-01-15 22:30:01 SenderName"
    followed by message content on subsequent lines.
    """
    messages = []
    current = None
    header_re = re.compile(
        r"^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}(?::\d{2})?)\s+(.+)$"
    )

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.rstrip("\n")
            m = header_re.match(line)
            if m:
                if current:
                    messages.append(current)
                ts, sender = m.groups()
                current = {"timestamp": ts, "sender": sender.strip(), "content": ""}
            elif current is not None and line.strip():
                sep = "\n" if current["content"] else ""
                current["content"] += sep + line

    if current:
        messages.append(current)

    return analyze_messages(messages, target_name)


def parse_bracket_txt(file_path: str, target_name: str) -> dict:
    """
    Parse bracket-style txt format.
    Line format: "[2024-01-15 22:30] sender: content"
    """
    messages = []
    line_re = re.compile(
        r"^\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}(?::\d{2})?)\]\s+(.+?):\s*(.*)$"
    )

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = line_re.match(line.strip())
            if m:
                ts, sender, content = m.groups()
                messages.append({
                    "timestamp": ts,
                    "sender": sender.strip(),
                    "content": content.strip(),
                })

    return analyze_messages(messages, target_name)


def parse_liuhen_json(file_path: str, target_name: str) -> dict:
    """Parse Liuhen JSON export (macOS app)."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    msg_list = (
        data if isinstance(data, list)
        else data.get("messages", data.get("data", []))
    )
    messages = []
    for msg in msg_list:
        messages.append({
            "timestamp": str(msg.get("time", msg.get("timestamp", ""))),
            "sender": str(msg.get(
                "sender", msg.get("nickname", msg.get("from", ""))
            )),
            "content": str(msg.get(
                "content", msg.get("message", msg.get("text", ""))
            )),
        })

    return analyze_messages(messages, target_name)


def parse_plaintext(file_path: str, target_name: str) -> dict:
    """
    Parse pasted plaintext chat logs.
    Attempts to match "sender: content" per line.
    Falls back to returning raw text if structure cannot be inferred.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    messages = []
    line_re = re.compile(r"^(.{1,20})[:]\s*(.+)$")
    for line in content.splitlines():
        m = line_re.match(line.strip())
        if m:
            sender, msg_content = m.groups()
            messages.append({
                "timestamp": "",
                "sender": sender.strip(),
                "content": msg_content.strip(),
            })

    if len(messages) >= 3:
        return analyze_messages(messages, target_name)

    # Cannot parse structure; return raw text for direct LLM reading
    return {
        "target_name": target_name,
        "total_messages": 0,
        "target_messages": 0,
        "user_messages": 0,
        "raw_text": content,
        "analysis": {
            "note": "Unstructured format. Raw content preserved for direct analysis.",
            "top_particles": [],
            "top_emojis": [],
            "avg_message_length": 0,
            "punctuation_habits": {},
            "message_style": "raw",
        },
        "sample_messages": [],
    }


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def analyze_messages(messages: list, target_name: str) -> dict:
    """
    Extract stylistic features from the target's messages.
    Returns a structured dict for downstream use by crush.skill.
    """
    target_msgs = [m for m in messages if target_name in m.get("sender", "")]
    user_msgs   = [m for m in messages if target_name not in m.get("sender", "")]

    all_text = " ".join(m["content"] for m in target_msgs if m.get("content"))

    # High-frequency filler particles
    particles = re.findall(r"[哈嗯哦噢嘿唉呜啊呀吧嘛呢吗么]+", all_text)
    particle_freq: dict = {}
    for p in particles:
        particle_freq[p] = particle_freq.get(p, 0) + 1
    top_particles = sorted(particle_freq.items(), key=lambda x: -x[1])[:10]

    # High-frequency emoji
    emoji_re = re.compile(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
        r"\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF"
        r"\U00002702-\U000027B0\U0000FE00-\U0000FE0F"
        r"\U0001F900-\U0001F9FF]+",
        re.UNICODE,
    )
    emojis = emoji_re.findall(all_text)
    emoji_freq: dict = {}
    for e in emojis:
        emoji_freq[e] = emoji_freq.get(e, 0) + 1
    top_emojis = sorted(emoji_freq.items(), key=lambda x: -x[1])[:10]

    # Average message length
    lengths = [len(m["content"]) for m in target_msgs if m.get("content")]
    avg_length = round(sum(lengths) / len(lengths), 1) if lengths else 0

    # Punctuation habits
    punctuation = {
        "period":           all_text.count("。"),
        "exclamation":      all_text.count("!") + all_text.count("！"),
        "question":         all_text.count("?") + all_text.count("？"),
        "ellipsis":         all_text.count("...") + all_text.count("…"),
        "tilde":            all_text.count("~") + all_text.count("～"),
    }

    return {
        "target_name": target_name,
        "total_messages": len(messages),
        "target_messages": len(target_msgs),
        "user_messages": len(user_msgs),
        "analysis": {
            "top_particles": top_particles,
            "top_emojis": top_emojis,
            "avg_message_length": avg_length,
            "punctuation_habits": punctuation,
            "message_style": "short_burst" if avg_length < 20 else "long_form",
        },
        "sample_messages": [
            m["content"] for m in target_msgs[:50] if m.get("content")
        ],
    }


# ---------------------------------------------------------------------------
# Output writer
# ---------------------------------------------------------------------------

def write_output(result: dict, output_path: str, fmt: str) -> None:
    """Write the analysis result to a Markdown file."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    target   = result.get("target_name", "unknown")
    analysis = result.get("analysis", {})

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Chat Analysis: {target}\n\n")
        f.write(f"Source format: {fmt}\n")
        f.write(f"Total messages: {result.get('total_messages', 'N/A')}\n")
        f.write(f"Messages from target: {result.get('target_messages', 'N/A')}\n")
        f.write(f"Messages from user: {result.get('user_messages', 'N/A')}\n\n")

        if analysis.get("note"):
            f.write(f"> Note: {analysis['note']}\n\n")

        if result.get("raw_text"):
            f.write("## Raw Chat Content\n\n```\n")
            f.write(result["raw_text"][:5000])
            if len(result["raw_text"]) > 5000:
                f.write("\n... (truncated)\n")
            f.write("```\n\n")

        if analysis.get("top_particles"):
            f.write("## Filler Particles (verbal habits)\n\n")
            for word, count in analysis["top_particles"]:
                f.write(f"- `{word}`: {count} occurrences\n")
            f.write("\n")

        if analysis.get("top_emojis"):
            f.write("## Frequent Emoji\n\n")
            for emoji, count in analysis["top_emojis"]:
                f.write(f"- {emoji}: {count} occurrences\n")
            f.write("\n")

        if any(v > 0 for v in analysis.get("punctuation_habits", {}).values()):
            f.write("## Punctuation Habits\n\n")
            for punct, count in analysis["punctuation_habits"].items():
                f.write(f"- {punct}: {count}\n")
            f.write("\n")

        f.write("## Message Style\n\n")
        f.write(f"- Average message length: {analysis.get('avg_message_length', 'N/A')} characters\n")
        style_map = {
            "short_burst": "short burst (multiple short messages)",
            "long_form":   "long form (paragraphs)",
            "raw":         "raw text",
        }
        style = style_map.get(analysis.get("message_style", ""), "unknown")
        f.write(f"- Style: {style}\n\n")

        if result.get("sample_messages"):
            f.write("## Sample Messages (first 50 from target)\n\n")
            for i, msg in enumerate(result["sample_messages"], 1):
                f.write(f"{i}. {msg}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Chat log parser for crush.skill"
    )
    parser.add_argument("--file",   required=True, help="Input file path")
    parser.add_argument("--target", required=True, help="Target person's name or nickname")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument(
        "--format", default="auto",
        help="File format: auto / wechatmsg_txt / bracket_txt / liuhen / plaintext",
    )
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    fmt = args.format
    if fmt == "auto":
        fmt = detect_format(args.file)
        print(f"Detected format: {fmt}")

    dispatch = {
        "wechatmsg_txt": parse_wechatmsg_txt,
        "bracket_txt":   parse_bracket_txt,
        "liuhen":        parse_liuhen_json,
        "plaintext":     parse_plaintext,
    }
    parse_fn = dispatch.get(fmt, parse_plaintext)
    result = parse_fn(args.file, args.target)

    write_output(result, args.output, fmt)
    print(f"Analysis complete. Output written to: {args.output}")
    print(
        f"Target messages: {result.get('target_messages', 'N/A')} "
        f"/ Total: {result.get('total_messages', 'N/A')}"
    )


if __name__ == "__main__":
    main()
