#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.umbrella_deps import load_updates, write_github_output_multiline


def main() -> int:
    updates = load_updates()

    commit_lines = [
        f"- {update['chart']}: {update['current']} -> {update['latest']}" for update in updates
    ]
    body_lines = [
        "Automated update of umbrella chart dependencies.",
        "",
        "The following subchart dependencies have been updated:",
        "",
    ]
    for update in updates:
        body_lines.append(f"- **{update['chart']}**: {update['current']} → {update['latest']}")
    body_lines.extend(
        [
            "",
            "The umbrella chart version has been bumped accordingly.",
            "",
            "This PR was automatically created by the update-umbrella-deps workflow.",
        ]
    )

    commit_msg = "chore: update umbrella chart dependencies\n\n" + "\n".join(commit_lines)
    pr_body = "\n".join(body_lines)

    write_github_output_multiline("commit_message", commit_msg)
    write_github_output_multiline("pr_body", pr_body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
