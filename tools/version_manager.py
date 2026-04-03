#!/usr/bin/env python3
"""
version_manager.py

Manages versions of the generated crush.skill files, allowing users to
save snapshots and rollback to previous states.

Usage:
    python3 version_manager.py --action save --slug <slug> --message <msg>
    python3 version_manager.py --action list --slug <slug>
    python3 version_manager.py --action rollback --slug <slug> --version <v>
"""

import argparse
import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path


def get_versions_dir(slug: str) -> Path:
    return Path(f"./crushes/{slug}/versions")


def save_version(slug: str, message: str):
    """Save a snapshot of the current skill files."""
    base_dir = Path(f"./crushes/{slug}")
    if not base_dir.exists():
        print(f"Error: crush '{slug}' does not exist.")
        return
    
    versions_dir = get_versions_dir(slug)
    versions_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_id = f"v_{timestamp}"
    version_dir = versions_dir / version_id
    version_dir.mkdir()
    
    # Copy files
    files_to_copy = ['SKILL.md', 'memory.md', 'persona.md', 'meta.json']
    for f in files_to_copy:
        src = base_dir / f
        if src.exists():
            shutil.copy2(src, version_dir / f)
    
    # Save metadata
    meta = {
        'version_id': version_id,
        'timestamp': timestamp,
        'message': message
    }
    with open(version_dir / 'version_meta.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"Version {version_id} saved: {message}")


def list_versions(slug: str):
    """List all saved versions."""
    versions_dir = get_versions_dir(slug)
    if not versions_dir.exists():
        print(f"No versions found for '{slug}'.")
        return
    
    versions = []
    for item in versions_dir.iterdir():
        if item.is_dir() and (item / 'version_meta.json').exists():
            with open(item / 'version_meta.json', 'r', encoding='utf-8') as f:
                meta = json.load(f)
                versions.append(meta)
    
    if not versions:
        print(f"No versions found for '{slug}'.")
        return
    
    versions.sort(key=lambda x: x['timestamp'], reverse=True)
    print(f"Versions for '{slug}':")
    for v in versions:
        print(f"- {v['version_id']} ({v['timestamp']}): {v['message']}")


def rollback_version(slug: str, version_id: str):
    """Rollback to a specific version."""
    base_dir = Path(f"./crushes/{slug}")
    version_dir = get_versions_dir(slug) / version_id
    
    if not version_dir.exists():
        print(f"Error: Version '{version_id}' does not exist.")
        return
    
    # Backup current state before rollback
    save_version(slug, f"Auto-backup before rollback to {version_id}")
    
    # Restore files
    files_to_restore = ['SKILL.md', 'memory.md', 'persona.md', 'meta.json']
    for f in files_to_restore:
        src = version_dir / f
        dst = base_dir / f
        if src.exists():
            shutil.copy2(src, dst)
            print(f"Restored {f}")
    
    print(f"Successfully rolled back to {version_id}")


def main():
    parser = argparse.ArgumentParser(description='Version Manager for crush.skill')
    parser.add_argument('--action', required=True, choices=['save', 'list', 'rollback'])
    parser.add_argument('--slug', required=True, help='The crush slug (e.g., xiaoming)')
    parser.add_argument('--message', default='Manual save', help='Commit message for save action')
    parser.add_argument('--version', help='Version ID for rollback action')
    
    args = parser.parse_args()
    
    if args.action == 'save':
        save_version(args.slug, args.message)
    elif args.action == 'list':
        list_versions(args.slug)
    elif args.action == 'rollback':
        if not args.version:
            print("Error: --version is required for rollback action.")
            sys.exit(1)
        rollback_version(args.slug, args.version)


if __name__ == '__main__':
    main()
