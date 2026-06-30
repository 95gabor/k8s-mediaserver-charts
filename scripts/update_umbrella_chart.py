#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.umbrella_deps import apply_umbrella_dependency_updates


def main() -> int:
    apply_umbrella_dependency_updates()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
