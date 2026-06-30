# k8s-mediaserver

Your all-in-one Helm chart for your media needs!

A Helm chart for deploying a complete media server stack on Kubernetes, including:

- [Plex Media Server](https://www.plex.tv/) - A complete and fully functional mediaserver that allows you to render in a webUI your movies, TV Series, podcasts, video streams.
- [Jellyfin](https://jellyfin.org/) - An alternative to the proprietary Emby and Plex, to provide media from a dedicated server to end-user devices via multiple apps
- [Sonarr](https://sonarr.tv/) - A TV series and show tracker, that allows the integration with download managers for searching and retrieving TV Series, organizing them, schedule notifications when an episode comes up and much more.
- [Radarr](https://radarr.video/) - The same as **Sonarr**, but for movies!
- [Jackett](https://github.com/Jackett/Jackett) - An API interface that keeps easy your life interacting with trackers for torrents.
- [Prowlarr](https://github.com/Prowlarr/Prowlarr) - An indexer manager/proxy built on the popular \*arr .net/reactjs base stack to integrate with your various PVR apps. Prowlarr supports management of both Torrent Trackers and Usenet Indexers.
- [Transmission](https://transmissionbt.com/) - A fast, easy and reliable torrent client.
- [Sabnzbd](https://sabnzbd.org/) - A free and easy binary newsreader.
- [Seerr](https://github.com/seerr-team/seerr) - Media request and discovery manager for Jellyfin, Plex, and Emby.

## Chart Structure

This repository contains:

- **Umbrella Chart** (`k8s-mediaserver`) - Deploys all services together with shared configuration
- **Individual Service Charts** - Each service (sonarr, radarr, plex, etc.) can be installed independently

All container images used by the chart are from [linuxserver.io](https://www.linuxserver.io/) except Seerr which uses the official image from [seerr-team](https://github.com/seerr-team/seerr).

Each of the components can be **enabled** or **disabled** if you already have something in place in your lab!

## Introduction

This Helm chart provides a simple and minimalistic way to deploy a complete media server stack on Kubernetes, with customizations that are strictly related to usability and access, rather than complex customizations.

Each container has its _init container_ in order to initialize configurations on the PV before starting the actual pod and avoid restarting the pods.

The chart is structured as an umbrella chart with individual service charts as dependencies, allowing you to:
- Install all services together with shared configuration
- Install individual services independently
- Mix and match services as needed

## Prerequisites

- A Kubernetes cluster (1.19+)
- Helm 3.x
- A namespace where you want to deploy the chart
- Being able to provision an RWX PV where to store configurations, downloads, and all related stuff (suggested > 200GB). Persistent Volume **or** StorageClasses for dynamically provisioned volumes are **REQUIRED** (See below for NFS)

## QuickStart

### Installation

#### Option 1: Install All Services (Umbrella Chart)

1. Add the Helm repository (if using a chart repository):

```bash
helm repo add k8s-mediaserver-charts https://95gabor.github.io/k8s-mediaserver-charts
helm repo update
```

2. Install the umbrella chart with default values:

```bash
# Using local chart directory
helm dependency update ./charts/k8s-mediaserver
helm upgrade --install k8s-mediaserver ./charts/k8s-mediaserver \
  -n k8s-mediaserver --create-namespace

# Or from chart repository
helm upgrade --install k8s-mediaserver k8s-mediaserver-charts/k8s-mediaserver \
  -n k8s-mediaserver --create-namespace
```

3. (Optional) Use custom values:

```bash
# Copy the default values file
cp ./charts/k8s-mediaserver/values.yaml my-values.yaml

# Edit my-values.yaml with your custom settings

# Install with custom values
helm dependency update ./charts/k8s-mediaserver
helm upgrade --install k8s-mediaserver ./charts/k8s-mediaserver \
  -n k8s-mediaserver --create-namespace \
  -f my-values.yaml
```

#### Option 2: Install Individual Services

You can also install individual service charts independently:

```bash
# Example: Install only Sonarr
helm upgrade --install sonarr ./charts/sonarr \
  -n sonarr --create-namespace \
  -f ./charts/sonarr/values.yaml

# Example: Install only Plex
helm upgrade --install plex ./charts/plex \
  -n plex --create-namespace \
  -f ./charts/plex/values.yaml
```

See the [charts README](charts/README.md) for a complete list of available charts.

### Upgrading

```bash
# Update dependencies first
helm dependency update ./charts/k8s-mediaserver

# Then upgrade
helm upgrade k8s-mediaserver ./charts/k8s-mediaserver \
  -n k8s-mediaserver \
  -f my-values.yaml
```

### Uninstalling

```bash
# Uninstall umbrella chart (removes all services)
helm uninstall k8s-mediaserver -n k8s-mediaserver

# Or uninstall individual services
helm uninstall sonarr -n sonarr
```

## Default Access URLs

With default settings, your applications will run at these paths:

| Service      | Link                                         |
| ------------ | -------------------------------------------- |
| Sonarr       | http://k8s-mediaserver.k8s.test/sonarr       |
| Radarr       | http://k8s-mediaserver.k8s.test/radarr      |
| Transmission | http://k8s-mediaserver.k8s.test/transmission |
| Jackett      | http://k8s-mediaserver.k8s.test/jackett      |
| Prowlarr     | http://k8s-mediaserver.k8s.test/prowlarr     |
| Sabnzbd      | http://k8s-mediaserver.k8s.test/sabnzbd      |
| Seerr        | http://k8s-mediaserver.k8s.test/seerr        |
| Jellyfin     | http://k8s-jelly.k8s.test/                   |
| PLEX         | http://k8s-plex.k8s.test/                    |

## Configuration

The chart is quite simple to configure, with a low number of parameters to avoid confusion, while still allowing customization to fit the resources inside your cluster.

> **Note:** The umbrella chart (`k8s-mediaserver`) only contains overrides and service-specific configurations. For complete documentation of all available values for each service chart, see the individual chart directories:
> - [sonarr](charts/sonarr/)
> - [radarr](charts/radarr/)
> - [jackett](charts/jackett/)
> - [prowlarr](charts/prowlarr/)
> - [transmission](charts/transmission/)
> - [sabnzbd](charts/sabnzbd/)
> - [plex](charts/plex/)
> - [jellyfin](charts/jellyfin/)
> - [seerr](charts/seerr/)

See the [values.yaml](charts/k8s-mediaserver/values.yaml) file for umbrella chart configuration options, or check the [Helm chart README](charts/k8s-mediaserver/README.md) for detailed documentation.

### General Configuration

Key configuration options:

- `general.ingress_host` - The hostname to use in ingress definition (default: `k8s-mediaserver.k8s.test`)
- `general.plex_ingress_host` - The hostname for PLEX (default: `k8s-plex.k8s.test`)
- `general.jellyfin_ingress_host` - The hostname for JellyFin (default: `k8s-jelly.k8s.test`)
- `general.pgid` - The GID for the process (default: `1000`)
- `general.puid` - The UID for the process (default: `1000`)
- `general.storage.pvcName` - Name of the persistentVolumeClaim (default: `mediaserver-pvc`)
- `general.storage.size` - Size of the persistentVolume (default: `5Gi`)
- `general.storage.subPaths.*` - Subpaths for different media types

### Service Configuration

Each service can be enabled/disabled and configured individually:

- `{service}.enabled` - Enable or disable the service
- `{service}.container.image` - Container image
- `{service}.container.tag` - Container image tag (pinned versions recommended)
- `{service}.service.type` - Service type (ClusterIP/NodePort/LoadBalancer)
- `{service}.ingress.enabled` - Enable ingress
- `{service}.resources` - Resource limits and requests

## Available Charts

This repository contains the following Helm charts:

- **[k8s-mediaserver](charts/k8s-mediaserver)** - Umbrella chart (deploys all services)
- **[sonarr](charts/sonarr)** - TV series tracker
- **[radarr](charts/radarr)** - Movie tracker
- **[plex](charts/plex)** - Media server
- **[jellyfin](charts/jellyfin)** - Alternative media server
- **[jackett](charts/jackett)** - Torrent tracker API
- **[prowlarr](charts/prowlarr)** - Indexer manager
- **[transmission](charts/transmission)** - Torrent client
- **[sabnzbd](charts/sabnzbd)** - Usenet client
- **[seerr](charts/seerr)** - Media request manager

Each chart has its own README with detailed documentation. See [charts/README.md](charts/README.md) for more information.

## Helpful Use Cases

### Using a cluster-external NFS server

This assumes that you have a pre-configured NFS server set up on your network that is accessible from all nodes. If it is not accessible by all nodes, pods will not enter ready state when scheduled on nodes that do not have NFS access.

To add an NFS volume to each resource, edit your `values.yaml` to match the snippet below. You should change the `server:` and `path:` values to match your NFS.

```yaml
general:
  storage:
    customVolume: true
    volumes:
      nfs:
        server: { SERVER-IP }
        path: /mount/path/on/nfs/server/
```

### Adding annotations to the extra load balancer

If you need an extra load balancer on any service, you can either enable it like this:

```yaml
plex:
  service:
    extraLbService:
      enabled: true
```

or like this, if you need to add annotations to it (for use with cloud providers to configure the load balancer for example):

```yaml
plex:
  service:
    extraLbService:
      enabled: true
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-additional-resource-tags: "Key=Value"
```

## Development

### Setup Development Environment

1. **Install pre-commit:**

   ```bash
   pip install pre-commit
   ```

2. **Install git hooks:**

   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

   This will automatically run checks before each commit, including:
   - Conventional commit message validation
   - YAML syntax checking
   - Helm chart linting
   - Documentation generation
   - File formatting checks

3. **Run pre-commit on all files (optional):**

   ```bash
   pre-commit run --all-files
   ```

### Local testing and automation

- [KinD integration tests](test/README.md) — run the umbrella chart deploy smoke test locally with an isolated KinD cluster
- [Maintenance scripts](scripts/README.md) — run app version and umbrella dependency update scripts locally

### Development Workflow

#### Linting

```bash
pre-commit run --all-files
```

#### Template Rendering

```bash
helm template test-release ./charts/k8s-mediaserver -f ./charts/k8s-mediaserver/values.yaml
```

#### Packaging

```bash
helm package ./charts/k8s-mediaserver
```

#### Generating Documentation

```bash
helm-docs --chart-search-root=charts
```

### Commit Message Format

This project uses [Conventional Commits](https://www.conventionalcommits.org/). Commit messages should follow this format:

```
<type>(<scope>): <subject>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples:**
- `feat(seerr): add init container for permission setup`
- `fix(sonarr): correct ingress path configuration`
- `docs(readme): update installation instructions`

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Development setup
- Code style guidelines
- Pull request process
- Chart development guidelines

## Acknowledgments

Special thanks to [kubealex](https://github.com/kubealex) (Alessandro Rossi) for creating the original k8s-mediaserver project. This repository is a fork with enhancements including:

- Split into individual service charts with umbrella chart support
- Added Seerr media request manager
- Improved chart structure and maintainability
- Updated documentation and examples

## Contributors

- [kubealex](https://github.com/kubealex) - Original creator
- [95gabor](https://github.com/95gabor) - Maintainer and contributor

## About the Project

This project is intended as an exercise, and absolutely for fun.
This is not intended to promote piracy.

Also feel free to contribute and extend it!
