#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.chart_updates import find_available_updates, save_updates, write_github_output


def main() -> int:
    updates = find_available_updates()

    if updates:
        print(f"\n✅ Found {len(updates)} updates available")
        save_updates(updates)
        write_github_output("has_updates", "true")
        write_github_output("updates_count", str(len(updates)))
        return 0

    print("✅ All charts are up to date")
    write_github_output("has_updates", "false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
