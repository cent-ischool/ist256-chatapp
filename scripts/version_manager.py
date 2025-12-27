#!/usr/bin/env python3
"""
Version Management Utility for IST256 Chatapp

This script provides utilities for managing version documentation,
including validation, listing, and cleanup operations.

Usage:
    python scripts/version_manager.py list
    python scripts/version_manager.py validate 1.0.2
    python scripts/version_manager.py current
    python scripts/version_manager.py set 1.0.2
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

# Base paths
PROJECT_ROOT = Path("/workspaces/ist256-chatapp")
CONSTANTS_FILE = PROJECT_ROOT / "app/chat/constants.py"
VERSIONS_DIR = PROJECT_ROOT / "docs/versions"
REQUIREMENTS_FILE = PROJECT_ROOT / "docs/project_requirements.md"

def get_current_version():
    """Extract current version from constants.py"""
    if not CONSTANTS_FILE.exists():
        print(f"Error: {CONSTANTS_FILE} not found")
        return None

    with open(CONSTANTS_FILE, 'r') as f:
        content = f.read()
        match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    return None

def set_version(new_version):
    """Update version in constants.py"""
    if not CONSTANTS_FILE.exists():
        print(f"Error: {CONSTANTS_FILE} not found")
        return False

    with open(CONSTANTS_FILE, 'r') as f:
        content = f.read()

    # Check if VERSION exists
    if 'VERSION' not in content:
        print(f"Error: VERSION constant not found in {CONSTANTS_FILE}")
        return False

    # Replace VERSION value
    updated = re.sub(
        r'VERSION\s*=\s*["\'][^"\']+["\']',
        f'VERSION="{new_version}"',
        content
    )

    with open(CONSTANTS_FILE, 'w') as f:
        f.write(updated)

    print(f"✅ Updated VERSION to {new_version} in {CONSTANTS_FILE}")
    return True

def list_versions():
    """List all documented versions"""
    if not VERSIONS_DIR.exists():
        print("No versions directory found")
        return

    versions = []
    for version_dir in sorted(VERSIONS_DIR.iterdir()):
        if version_dir.is_dir() and version_dir.name.startswith('v'):
            version = version_dir.name
            has_spec = (version_dir / "technical-spec.md").exists()
            has_plan = (version_dir / "implementation-plan.md").exists()

            versions.append({
                'version': version,
                'has_spec': has_spec,
                'has_plan': has_plan,
                'complete': has_spec and has_plan
            })

    if not versions:
        print("No version documentation found in docs/versions/")
        return

    print("\n" + "="*60)
    print("VERSION DOCUMENTATION STATUS")
    print("="*60)
    for v in versions:
        status = "✅ Complete" if v['complete'] else "❌ Incomplete"
        spec = "✅" if v['has_spec'] else "❌"
        plan = "✅" if v['has_plan'] else "❌"
        print(f"{v['version']:10} {status:17} [Spec: {spec}] [Plan: {plan}]")
    print("="*60 + "\n")

def validate_version(version):
    """Validate that a version has all required documentation"""
    version_dir = VERSIONS_DIR / f"v{version}"

    if not version_dir.exists():
        print(f"❌ Version directory not found: {version_dir}")
        return False

    spec_file = version_dir / "technical-spec.md"
    plan_file = version_dir / "implementation-plan.md"

    issues = []

    if not spec_file.exists():
        issues.append("Missing technical-spec.md")

    if not plan_file.exists():
        issues.append("Missing implementation-plan.md")

    if issues:
        print(f"❌ Version v{version} validation failed:")
        for issue in issues:
            print(f"   - {issue}")
        return False

    print(f"✅ Version v{version} is valid and complete")
    return True

def check_requirements_for_version(version):
    """Check if version exists in project_requirements.md"""
    if not REQUIREMENTS_FILE.exists():
        print(f"Error: {REQUIREMENTS_FILE} not found")
        return False

    with open(REQUIREMENTS_FILE, 'r') as f:
        content = f.read()

    # Look for version header
    patterns = [
        f"##\\s+v{version}",
        f"##\\s+{version}",
        f"###\\s+v{version}",
    ]

    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            print(f"✅ Found requirements for v{version} in project_requirements.md")
            return True

    print(f"❌ No requirements found for v{version} in project_requirements.md")
    return False

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "current":
        version = get_current_version()
        if version:
            print(f"Current version: {version}")
        else:
            print("Could not determine current version")

    elif command == "list":
        list_versions()

    elif command == "validate":
        if len(sys.argv) < 3:
            print("Usage: version_manager.py validate <version>")
            sys.exit(1)
        version = sys.argv[2]
        valid = validate_version(version)
        has_reqs = check_requirements_for_version(version)
        if valid and has_reqs:
            print(f"\n✅ Version v{version} is fully documented and ready")
        sys.exit(0 if (valid and has_reqs) else 1)

    elif command == "set":
        if len(sys.argv) < 3:
            print("Usage: version_manager.py set <version>")
            sys.exit(1)
        version = sys.argv[2]
        success = set_version(version)
        sys.exit(0 if success else 1)

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
