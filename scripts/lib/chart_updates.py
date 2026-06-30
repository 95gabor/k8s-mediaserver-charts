from __future__ import annotations

import json
import os
import re
from pathlib import Path

import requests
import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "chart-updates.yaml"
CHARTS_DIR = Path("charts")
UPDATES_FILE = Path("updates.json")


def load_chart_configs() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as config_file:
        data = yaml.safe_load(config_file)
    return data["charts"]


def get_latest_release(repo: str) -> dict | None:
    response = requests.get(
        f"https://api.github.com/repos/{repo}/releases/latest",
        timeout=30,
    )
    if response.status_code == 200:
        return response.json()
    return None


def get_commit_hash_from_release(release: dict | None) -> str | None:
    if not release:
        return None

    if "target_commitish" in release:
        commit_ref = release["target_commitish"]
        if len(commit_ref) == 40:
            return commit_ref[:7]

    if "tag_name" not in release:
        return None

    tag_name = release["tag_name"]
    repo = None
    if "/repos/" in release.get("url", ""):
        repo = release["url"].split("/repos/")[1].split("/releases")[0]

    if not repo:
        return None

    tag_response = requests.get(
        f"https://api.github.com/repos/{repo}/git/refs/tags/{tag_name}",
        timeout=30,
    )
    if tag_response.status_code == 200:
        tag_data = tag_response.json()
        if "object" in tag_data and "sha" in tag_data["object"]:
            return tag_data["object"]["sha"][:7]

    commits_response = requests.get(
        f"https://api.github.com/repos/{repo}/commits/{tag_name}",
        timeout=30,
    )
    if commits_response.status_code == 200:
        commit_data = commits_response.json()
        if "sha" in commit_data:
            return commit_data["sha"][:7]

    return None


def extract_base_version(version_string: str) -> str:
    parts = version_string.split(".")
    if len(parts) >= 3:
        return ".".join(parts[:3])
    return version_string


def extract_linuxserver_app_version(version_string: str) -> str | None:
    match = re.match(r"^(\d+\.\d+\.\d+)", version_string.lstrip("v"))
    return match.group(1) if match else None


def docker_hub_tag_exists(image: str, tag: str) -> bool:
    if "/" not in image:
        return False

    namespace, repository = image.split("/", 1)
    response = requests.get(
        f"https://hub.docker.com/v2/repositories/{namespace}/{repository}/tags/{tag}",
        timeout=30,
    )
    return response.status_code == 200


def get_latest_container_tag(container_registry: str) -> str | None:
    if not container_registry:
        return None

    parts = container_registry.replace("ghcr.io/", "").split("/")
    if len(parts) != 2:
        return None

    org, package = parts
    url = f"https://api.github.com/orgs/{org}/packages/container/{package}/versions"
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        print(
            f"⚠️  Failed to fetch container tags: {response.status_code} - {response.text[:200]}"
        )
        return None

    sha_tags = []
    for version in response.json():
        if "metadata" not in version or "container" not in version["metadata"]:
            continue
        tags = version["metadata"]["container"].get("tags", [])
        for tag in tags:
            if tag.startswith("sha-"):
                sha_tags.append(
                    {
                        "tag": tag,
                        "updated_at": version.get("updated_at", ""),
                    }
                )

    if not sha_tags:
        return None

    sha_tags.sort(key=lambda item: item["updated_at"], reverse=True)
    return sha_tags[0]["tag"]


def resolve_latest_version(chart_name: str, config: dict, release: dict) -> str | None:
    tag_format = config["tag_format"]
    latest_tag = release["tag_name"].lstrip("v")

    if tag_format == "container_registry":
        return get_latest_container_tag(config.get("container_registry"))

    if tag_format == "version_base":
        return extract_base_version(latest_tag)

    if tag_format == "linuxserver_app_version":
        return extract_linuxserver_app_version(latest_tag)

    return latest_tag


def validate_docker_image(chart_name: str, config: dict, version: str) -> bool:
    docker_image = config.get("docker_image")
    if not docker_image:
        return True

    if docker_hub_tag_exists(docker_image, version):
        return True

    print(
        f"⚠️  {chart_name}: Docker image {docker_image}:{version} is not published yet, skipping"
    )
    return False


def find_available_updates() -> list[dict]:
    updates = []

    for chart_name, config in load_chart_configs().items():
        chart_path = CHARTS_DIR / chart_name / "Chart.yaml"
        if not chart_path.exists():
            continue

        with open(chart_path, encoding="utf-8") as chart_file:
            chart_data = yaml.safe_load(chart_file)

        current_app_version = chart_data.get("appVersion", "")
        release = get_latest_release(config["repo"])
        if not release:
            continue

        latest_version = resolve_latest_version(chart_name, config, release)
        if not latest_version or latest_version == current_app_version:
            continue

        if not validate_docker_image(chart_name, config, latest_version):
            continue

        updates.append(
            {
                "chart": chart_name,
                "current": current_app_version,
                "latest": latest_version,
                "release_url": release["html_url"],
            }
        )
        print(f"📦 {chart_name}: {current_app_version} -> {latest_version}")

    return updates


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


def save_updates(updates: list[dict]) -> None:
    with open(UPDATES_FILE, "w", encoding="utf-8") as updates_file:
        json.dump(updates, updates_file, indent=2)


def load_updates() -> list[dict]:
    with open(UPDATES_FILE, encoding="utf-8") as updates_file:
        return json.load(updates_file)
