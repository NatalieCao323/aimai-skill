"""
skill_writer.py

File management utility for crush.skill.

Manages the crushes/ directory: listing, validating, and cleaning up
generated crush Skill files.

Usage:
  python3 skill_writer.py --action list
  python3 skill_writer.py --action list --base-dir ./crushes
"""

import argparse
import os
import sys
from pathlib import Path


def list_skills(base_dir: str) -> None:
    """List all generated crush Skill directories."""
    base_path = Path(base_dir)

    if not base_path.exists():
        print("No crush Skills found.")
        return

    skills = [
        item.name
        for item in sorted(base_path.iterdir())
        if item.is_dir() and (item / "SKILL.md").exists()
    ]

    if not skills:
        print("No crush Skills found.")
        return

    print(f"Generated crush Skills ({len(skills)} total):")
    for slug in skills:
        skill_path = base_path / slug / "SKILL.md"
        size = skill_path.stat().st_size
        print(f"  {slug}  ({size} bytes)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="File management utility for crush.skill"
    )
    parser.add_argument(
        "--action", required=True, choices=["list"],
        help="Action to perform"
    )
    parser.add_argument(
        "--base-dir", default="./crushes",
        help="Base directory for crush Skill files (default: ./crushes)"
    )

    args = parser.parse_args()

    if args.action == "list":
        list_skills(args.base_dir)


if __name__ == "__main__":
    main()
