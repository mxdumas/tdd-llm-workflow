#!/usr/bin/env python3
"""Generate manifest.json for templates directory.

This script scans the templates directory and generates a manifest.json file
containing version information and SHA256 checksums for all template files.

Usage:
    python scripts/generate_manifest.py <version>

Example:
    python scripts/generate_manifest.py 1.0.0
"""

import hashlib
import json
import sys
from pathlib import Path


def generate_manifest(templates_dir: Path, version: str) -> dict:
    """Generate manifest from templates directory.

    Args:
        templates_dir: Path to templates directory.
        version: Version string for the manifest.

    Returns:
        Dict with version and templates mapping paths to checksums.
    """
    templates = {}

    for file_path in sorted(templates_dir.rglob("*")):
        if file_path.is_file() and file_path.name != "manifest.json":
            rel_path = file_path.relative_to(templates_dir).as_posix()
            content = file_path.read_bytes()
            checksum = hashlib.sha256(content).hexdigest()
            templates[rel_path] = checksum

    return {
        "version": version,
        "templates": templates
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_manifest.py <version>")
        print("Example: python scripts/generate_manifest.py 1.0.0")
        sys.exit(1)

    version = sys.argv[1]

    # Find templates directory relative to script location
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    templates_dir = project_root / "src" / "tdd_llm" / "templates"

    if not templates_dir.exists():
        print(f"Error: Templates directory not found: {templates_dir}")
        sys.exit(1)

    manifest = generate_manifest(templates_dir, version)

    # Write manifest to templates directory
    manifest_path = templates_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)

    print("Generated manifest.json:")
    print(f"  Version: {version}")
    print(f"  Files: {len(manifest['templates'])}")
    print(f"  Path: {manifest_path}")


if __name__ == "__main__":
    main()
