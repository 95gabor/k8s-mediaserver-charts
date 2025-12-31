# k8s-mediaserver

![Version: 0.10.24](https://img.shields.io/badge/Version-0.10.24-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 0.10.0](https://img.shields.io/badge/AppVersion-0.10.0-informational?style=flat-square)

A Helm chart for Kubernetes mediaserver (umbrella chart)

## Chart Repo

Add the following repo to use the chart:

```bash
helm repo add k8s-mediaserver-charts https://95gabor.github.io/k8s-mediaserver-charts
helm repo update
```

### Installation

- Install/upgrade in a namespace (using local chart directory):

```bash
helm upgrade --install k8s-mediaserver . \
  -n k8s-mediaserver --create-namespace \
  -f values.yaml
```

- Or install from a chart repository:

```bash
helm upgrade --install k8s-mediaserver k8s-mediaserver-charts/k8s-mediaserver \
  -n k8s-mediaserver --create-namespace \
  -f values.yaml
```

- Uninstall:

```bash
helm uninstall k8s-mediaserver -n k8s-mediaserver
```

## Service Chart Documentation

> **Note:** This umbrella chart only contains overrides and service-specific configurations.
> For complete documentation of all available values for each service chart, see the individual chart directories:
> - [sonarr](../sonarr/)
> - [radarr](../radarr/)
> - [jackett](../jackett/)
> - [prowlarr](../prowlarr/)
> - [transmission](../transmission/)
> - [sabnzbd](../sabnzbd/)
> - [plex](../plex/)
> - [jellyfin](../jellyfin/)
> - [seerr](../seerr/)

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| general.certificate.additionalHosts[0] | string | `"plex.example.com"` |  |
| general.certificate.additionalHosts[1] | string | `"sonarr.example.com"` |  |
| general.certificate.additionalHosts[2] | string | `"radarr.example.com"` |  |
| general.certificate.annotations | object | `{}` |  |
| general.certificate.domain | string | `"plex.example.com"` |  |
| general.certificate.duration | string | `""` |  |
| general.certificate.enabled | bool | `false` |  |
| general.certificate.issuer.group | string | `""` |  |
| general.certificate.issuer.kind | string | `""` |  |
| general.certificate.issuer.name | string | `""` |  |
| general.certificate.keystores.pkcs12.create | bool | `true` |  |
| general.certificate.keystores.pkcs12.passwordSecretRef.key | string | `"password"` |  |
| general.certificate.keystores.pkcs12.passwordSecretRef.name | string | `"cert-password"` |  |
| general.certificate.privateKey.algorithm | string | `"RSA"` |  |
| general.certificate.privateKey.encoding | string | `"PKCS1"` |  |
| general.certificate.privateKey.rotationPolicy | string | `"Never"` |  |
| general.certificate.privateKey.size | int | `2048` |  |
| general.certificate.renewBefore | string | `""` |  |
| general.certificate.secretName | string | `"k8s-mediaserver-tls"` |  |
| general.certificate.usages | list | `[]` |  |
| general.ingress.ingressClassName | string | `""` |  |
| general.ingress_host | string | `"k8s-mediaserver.k8s.test"` |  |
| general.initContainer.image | string | `"docker.io/ubuntu"` |  |
| general.initContainer.runAsRoot | bool | `true` |  |
| general.initContainer.tag | float | `24.04` |  |
| general.jellyfin_ingress_host | string | `"k8s-jelly.k8s.test"` |  |
| general.nodeSelector | object | `{}` |  |
| general.plex_ingress_host | string | `"k8s-plex.k8s.test"` |  |
| general.podDistribution | string | `"cluster"` |  |
| general.storage.accessMode | string | `""` |  |
| general.storage.customVolume | bool | `false` |  |
| general.storage.pvcName | string | `"mediaserver-pvc"` |  |
| general.storage.pvcStorageClass | string | `""` |  |
| general.storage.size | string | `"5Gi"` |  |
| general.storage.subPaths.config | string | `"config"` |  |
| general.storage.subPaths.downloads | string | `"downloads"` |  |
| general.storage.subPaths.movies | string | `"media/movies"` |  |
| general.storage.subPaths.sabnzbd | string | `"sabnzbd"` |  |
| general.storage.subPaths.transmission | string | `"transmission"` |  |
| general.storage.subPaths.tv | string | `"media/tv"` |  |
| general.storage.volumes | object | `{}` |  |
| jackett.enabled | bool | `true` |  |
| jellyfin.enabled | bool | `false` |  |
| jellyfin.general.jellyfin_ingress_host | string | `"k8s-jelly.k8s.test"` |  |
| jellyfin.replicaCount | int | `1` |  |
| plex.claim | string | `"CHANGEME"` |  |
| plex.enabled | bool | `true` |  |
| plex.externalSecret | string | `nil` |  |
| plex.general.certificate.enabled | bool | `false` |  |
| plex.general.certificate.secretName | string | `"k8s-mediaserver-tls"` |  |
| plex.general.plex_ingress_host | string | `"k8s-plex.k8s.test"` |  |
| plex.replicaCount | int | `1` |  |
| prowlarr.enabled | bool | `true` |  |
| radarr.enabled | bool | `true` |  |
| sabnzbd.enabled | bool | `true` |  |
| seerr.enabled | bool | `true` |  |
| sonarr.enabled | bool | `true` |  |
| transmission.enabled | bool | `true` |  |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.14.2](https://github.com/norwoodj/helm-docs/releases/v1.14.2)
