# Local testing

Integration test assets for deploying the umbrella chart to a local [KinD](https://kind.sigs.k8s.io/) cluster.

This mirrors the `Helm Chart Tests` workflow in [`.github/workflows/integration-tests.yml`](../.github/workflows/integration-tests.yml).

## Prerequisites

- Docker
- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [helm](https://helm.sh/docs/intro/install/) 3.x
- `wget` and `sudo` (for endpoint checks via `/etc/hosts`)

## Important

Use a **dedicated KinD cluster** for testing. Do not run these steps against an existing home/production cluster.

Always verify your kubectl context before and after:

```bash
kubectl config current-context
```

After testing, delete the KinD cluster and switch back to your normal context.

## Quick start

From the repository root:

```bash
CLUSTER=mediaserver-test
ORIG_CTX=$(kubectl config current-context)

cleanup() {
  kind delete cluster --name "${CLUSTER}" 2>/dev/null || true
  kubectl config use-context "${ORIG_CTX}" 2>/dev/null || true
}
trap cleanup EXIT

kind create cluster --name "${CLUSTER}" --config test/kind/kind-config.yaml

helm repo add k8s-mediaserver-charts https://95gabor.github.io/k8s-mediaserver-charts
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm dependency update charts/k8s-mediaserver

helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --wait \
  --timeout 5m \
  -f test/kind/ingress-nginx-values.yaml

helm upgrade --install k8s-mediaserver ./charts/k8s-mediaserver \
  -n mediaserver \
  --create-namespace \
  --wait \
  --timeout 10m \
  -f test/kind/helm-values.yaml

test/kind/test-endpoints.sh
```

## Files

| File | Purpose |
|------|---------|
| [`kind/kind-config.yaml`](kind/kind-config.yaml) | KinD cluster config (ingress-ready node, ports 80/443) |
| [`kind/ingress-nginx-values.yaml`](kind/ingress-nginx-values.yaml) | ingress-nginx Helm values for KinD |
| [`kind/helm-values.yaml`](kind/helm-values.yaml) | Umbrella chart overrides for integration tests |
| [`kind/test-endpoints.sh`](kind/test-endpoints.sh) | HTTP smoke checks via ingress |

## Lint only

To run the workflow lint/template steps without KinD:

```bash
helm repo add k8s-mediaserver-charts https://95gabor.github.io/k8s-mediaserver-charts
helm repo update
helm dependency update charts/k8s-mediaserver
helm lint charts/k8s-mediaserver
helm template charts/k8s-mediaserver
```

## Endpoint test environment variables

`test-endpoints.sh` accepts:

| Variable | Default |
|----------|---------|
| `INGRESS_HOST` | `k8s-mediaserver.k8s.test` |
| `PLEX_INGRESS_HOST` | `k8s-plex.k8s.test` |
| `JELLYFIN_INGRESS_HOST` | `k8s-jelly.k8s.test` |

The script appends entries to `/etc/hosts` pointing at `127.0.0.1`.

## Cleanup

```bash
kind delete cluster --name mediaserver-test
kubectl config use-context <your-normal-context>
```

Remove any `/etc/hosts` lines added during testing if you no longer need them.
