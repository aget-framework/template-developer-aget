#!/usr/bin/env python3
"""Smart reader that handles both files and directories gracefully."""

import os
import json
from pathlib import Path


def safe_read(path):
    """
    Intelligently read a path - file contents or directory listing.
    Prevents EISDIR errors that agents encounter.
    """
    path = Path(path).expanduser().resolve()

    if path.is_dir():
        items = sorted(os.listdir(path))
        return {
            "type": "directory",
            "path": str(path),
            "contents": items,
            "message": f"Directory with {len(items)} items",
            "suggestion": f"To read a specific file, try: {path}/[filename]"
        }
    elif path.is_file():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {
                "type": "file",
                "path": str(path),
                "content": content,
                "lines": len(content.splitlines())
            }
        except Exception as e:
            return {
                "type": "error",
                "path": str(path),
                "error": str(e),
                "suggestion": "Check file permissions or encoding"
            }
    else:
        # Path doesn't exist - suggest similar paths
        parent = path.parent
        if parent.exists():
            similar = [p.name for p in parent.iterdir()
                      if path.name.lower() in p.name.lower()]
            return {
                "type": "not_found",
                "path": str(path),
                "suggestion": f"Did you mean: {similar[:3]}" if similar else "Check the path"
            }
        return {
            "type": "not_found",
            "path": str(path),
            "error": "Path does not exist"
        }


def find_docs(base_path="."):
    """Find all documentation directories in the project."""
    docs_dirs = []
    for root, dirs, files in os.walk(base_path):
        if 'docs' in dirs or 'documentation' in dirs:
            docs_dirs.append(os.path.join(root, 'docs') if 'docs' in dirs
                           else os.path.join(root, 'documentation'))
        # Don't go too deep
        if root.count(os.sep) - base_path.count(os.sep) >= 2:
            dirs.clear()
    return docs_dirs


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        result = safe_read(sys.argv[1])
        print(json.dumps(result, indent=2))
    else:
        print("Usage: smart_reader.py <path>")
        print("\nAvailable documentation:")
        for doc_dir in find_docs():
            print(f"  - {doc_dir}")