# Scripts

Python helpers used by GitHub Actions workflows for chart version maintenance.

## Prerequisites

- Python 3.10+
- Network access (GitHub API, Docker Hub)
- Run commands from the **repository root**

Optional:

- `GITHUB_TOKEN` — required for Seerr container registry lookups (`ghcr.io/seerr-team/seerr`)
- `GITHUB_OUTPUT` — set automatically in GitHub Actions; not needed locally

## Setup

```bash
python3 -m venv .venv-scripts
source .venv-scripts/bin/activate
pip install -r scripts/requirements.txt
```

## Configuration

Chart update sources live in [`config/chart-updates.yaml`](config/chart-updates.yaml). Each entry defines:

- `repo` — GitHub repository used to detect new releases
- `tag_format` — how the release tag is mapped to `appVersion`
- `docker_image` — when set, the bump is skipped unless this Docker Hub tag exists

## App version updates (`check-updates` workflow)

Check which charts have updates available:

```bash
python scripts/check_for_updates.py
```

If updates are found, `updates.json` is written in the repo root.

Apply the updates to `charts/*/Chart.yaml`:

```bash
python scripts/apply_chart_updates.py
```

Generate PR metadata (normally consumed by GitHub Actions):

```bash
python scripts/prepare_app_versions_pr.py
```

Dry-run example:

```bash
python scripts/check_for_updates.py
cat updates.json
# do not run apply_chart_updates.py unless you intend to modify charts
```

## Umbrella chart dependency updates (`update-umbrella-deps` workflow)

Check whether subchart versions differ from the umbrella chart dependencies:

```bash
python scripts/check_umbrella_deps.py
```

Apply dependency bumps to `charts/k8s-mediaserver/Chart.yaml`:

```bash
python scripts/update_umbrella_chart.py
```

Generate PR metadata:

```bash
python scripts/prepare_umbrella_pr.py
```

## Script reference

| Script | Purpose |
|--------|---------|
| `check_for_updates.py` | Detect app version bumps |
| `apply_chart_updates.py` | Write bumps to subchart `Chart.yaml` files |
| `prepare_app_versions_pr.py` | Build commit message and PR body |
| `check_umbrella_deps.py` | Detect umbrella dependency drift |
| `update_umbrella_chart.py` | Sync umbrella `Chart.yaml` dependencies |
| `prepare_umbrella_pr.py` | Build umbrella PR metadata |

Shared logic is in [`lib/`](lib/).

## Notes

- Scripts write `updates.json` to the repository root during CI. The file is gitignored.
- After applying chart changes locally, run `pre-commit run --all-files` before committing.
