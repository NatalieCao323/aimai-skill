#!/usr/bin/env python3
"""
qq_parser.py

Parses QQ chat exports (txt or mht formats) to extract the target's messages
and generate a structured analysis report.

Usage:
    python3 qq_parser.py --file <path> --target <name> --output <output_path>
"""

import argparse
import re
import os
import sys
from pathlib import Path


def parse_qq_txt(file_path: str, target_name: str) -> dict:
    """Parse QQ exported txt format."""
    messages = []
    current_msg = None
    
    # QQ timestamp + sender pattern
    msg_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)(?:\((\d+)\))?\s*$')
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.rstrip('\n')
            match = msg_pattern.match(line)
            if match:
                if current_msg:
                    messages.append(current_msg)
                timestamp, sender, qq_number = match.groups()
                current_msg = {
                    'timestamp': timestamp,
                    'sender': sender.strip(),
                    'content': ''
                }
            elif current_msg and line.strip() and not line.startswith('==='):
                if current_msg['content']:
                    current_msg['content'] += '\n'
                current_msg['content'] += line
    
    if current_msg:
        messages.append(current_msg)
    
    # Basic statistics
    target_msgs = [m for m in messages if target_name in m.get('sender', '')]
    all_target_text = ' '.join([m['content'] for m in target_msgs if m.get('content')])
    
    return {
        'target_name': target_name,
        'total_messages': len(messages),
        'target_messages': len(target_msgs),
        'sample_messages': [m['content'] for m in target_msgs[:50] if m.get('content')],
        'raw_text': all_target_text[:10000],
    }


def parse_qq_mht(file_path: str, target_name: str) -> dict:
    """Parse QQ exported mht format (HTML content)."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Strip HTML tags
    clean_text = re.sub(r'<[^>]+>', '\n', content)
    clean_text = re.sub(r'\n{3,}', '\n\n', clean_text)
    
    return {
        'target_name': target_name,
        'format': 'mht',
        'raw_text': clean_text[:20000],
        'note': 'MHT format detected. Extracted plain text.'
    }


def main():
    parser = argparse.ArgumentParser(description='QQ Chat Parser')
    parser.add_argument('--file', required=True, help='Input file path')
    parser.add_argument('--target', required=True, help='Target name/nickname')
    parser.add_argument('--output', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File does not exist: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    ext = Path(args.file).suffix.lower()
    if ext in ['.mht', '.mhtml']:
        result = parse_qq_mht(args.file, args.target)
    else:
        result = parse_qq_txt(args.file, args.target)
    
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(f"# QQ Chat Analysis — {args.target}\n\n")
        f.write(f"Total messages: {result.get('total_messages', 'N/A')}\n")
        f.write(f"Target messages: {result.get('target_messages', 'N/A')}\n\n")
        
        if result.get('sample_messages'):
            f.write("## Sample Messages\n")
            for i, msg in enumerate(result['sample_messages'], 1):
                f.write(f"{i}. {msg}\n")
        elif result.get('raw_text'):
            f.write("## Raw Text (Truncated)\n\n")
            f.write(result['raw_text'][:10000])
    
    print(f"Analysis complete. Results written to {args.output}")


if __name__ == '__main__':
    main()
