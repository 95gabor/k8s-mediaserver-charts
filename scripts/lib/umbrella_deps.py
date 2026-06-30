from __future__ import annotations

import json
import os
from pathlib import Path

import yaml

CHARTS_DIR = Path("charts")
UMBRELLA_CHART_PATH = CHARTS_DIR / "k8s-mediaserver" / "Chart.yaml"
UPDATES_FILE = Path("updates.json")


def write_github_output(name: str, value: str) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return

    with open(output_path, "a", encoding="utf-8") as output_file:
        output_file.write(f"{name}={value}\n")


def write_github_output_multiline(name: str, value: str) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return

    with open(output_path, "a", encoding="utf-8") as output_file:
        output_file.write(f"{name}<<EOF\n{value}\nEOF\n")


def find_umbrella_dependency_updates() -> list[dict]:
    updates = []

    with open(UMBRELLA_CHART_PATH, encoding="utf-8") as umbrella_file:
        umbrella_data = yaml.safe_load(umbrella_file)

    current_deps = {}
    if "dependencies" in umbrella_data:
        for dep in umbrella_data["dependencies"]:
            current_deps[dep["name"]] = dep.get("version", "")

    subchart_dirs = [
        chart_dir
        for chart_dir in CHARTS_DIR.iterdir()
        if chart_dir.is_dir() and chart_dir.name != "k8s-mediaserver"
    ]

    for subchart_dir in subchart_dirs:
        chart_path = subchart_dir / "Chart.yaml"
        if not chart_path.exists():
            continue

        chart_name = subchart_dir.name
        with open(chart_path, encoding="utf-8") as chart_file:
            chart_data = yaml.safe_load(chart_file)

        current_version = chart_data.get("version", "")
        if chart_name not in current_deps:
            continue

        umbrella_version = current_deps[chart_name]
        if current_version == umbrella_version:
            continue

        updates.append(
            {
                "chart": chart_name,
                "current": umbrella_version,
                "latest": current_version,
            }
        )
        print(f"📦 {chart_name}: {umbrella_version} -> {current_version}")

    return updates


def save_updates(updates: list[dict]) -> None:
    with open(UPDATES_FILE, "w", encoding="utf-8") as updates_file:
        json.dump(updates, updates_file, indent=2)


def load_updates() -> list[dict]:
    with open(UPDATES_FILE, encoding="utf-8") as updates_file:
        return json.load(updates_file)


def apply_umbrella_dependency_updates() -> None:
    with open(UPDATES_FILE, encoding="utf-8") as updates_file:
        updates = json.load(updates_file)

    with open(UMBRELLA_CHART_PATH, encoding="utf-8") as umbrella_file:
        umbrella_data = yaml.safe_load(umbrella_file)

    if "dependencies" in umbrella_data:
        for dep in umbrella_data["dependencies"]:
            chart_name = dep["name"]
            for update in updates:
                if update["chart"] == chart_name:
                    dep["version"] = update["latest"]
                    print(
                        f"Updated dependency {chart_name}: {update['current']} -> {update['latest']}"
                    )

    current_version = umbrella_data.get("version", "0.0.0")
    version_parts = current_version.split(".")
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    new_version = ".".join(version_parts)
    umbrella_data["version"] = new_version
    print(f"Bumped umbrella chart version: {current_version} -> {new_version}")

    with open(UMBRELLA_CHART_PATH, "w", encoding="utf-8") as umbrella_file:
        yaml.dump(
            umbrella_data,
            umbrella_file,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
