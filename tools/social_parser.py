#!/usr/bin/env python3
"""
social_parser.py

Parses social media text exports (e.g., Moments, Weibo) to extract
public persona and interests.

Usage:
    python3 social_parser.py --file <path> --output <output_path>
"""

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description='Social Media Parser')
    parser.add_argument('--file', required=True, help='Input text file path')
    parser.add_argument('--output', required=True, help='Output markdown file path')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File does not exist: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    with open(args.file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Basic keyword extraction for interests
    keywords = ['music', 'movie', 'game', 'food', 'travel', 'work', 'study', 'cat', 'dog']
    found_keywords = [kw for kw in keywords if kw in content.lower()]
    
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(f"# Social Media Analysis\n\n")
        f.write(f"Source file: {os.path.basename(args.file)}\n\n")
        
        f.write("## Potential Interests Detected\n")
        if found_keywords:
            for kw in found_keywords:
                f.write(f"- {kw.capitalize()}\n")
        else:
            f.write("- No obvious keywords detected.\n")
        
        f.write("\n## Raw Content (Truncated)\n\n")
        f.write(content[:5000])
    
    print(f"Analysis complete. Results written to {args.output}")


if __name__ == '__main__':
    main()
