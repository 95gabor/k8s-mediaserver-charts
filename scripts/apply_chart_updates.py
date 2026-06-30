#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.chart_updates import CHARTS_DIR, load_updates


def main() -> int:
    for update in load_updates():
        chart_path = CHARTS_DIR / update["chart"] / "Chart.yaml"
        with open(chart_path, encoding="utf-8") as chart_file:
            chart_data = yaml.safe_load(chart_file)

        chart_data["appVersion"] = update["latest"]
        version_parts = chart_data["version"].split(".")
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        chart_data["version"] = ".".join(version_parts)

        with open(chart_path, "w", encoding="utf-8") as chart_file:
            yaml.dump(chart_data, chart_file, default_flow_style=False, sort_keys=False)

        print(f"Updated {update['chart']}: {update['current']} -> {update['latest']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
