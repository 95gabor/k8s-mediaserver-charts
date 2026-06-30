#!/usr/bin/env bash
set -euo pipefail

ingress_host="${INGRESS_HOST:-k8s-mediaserver.k8s.test}"
plex_ingress_host="${PLEX_INGRESS_HOST:-k8s-plex.k8s.test}"
jellyfin_ingress_host="${JELLYFIN_INGRESS_HOST:-k8s-jelly.k8s.test}"

echo "127.0.0.1   ${plex_ingress_host} ${ingress_host}" | sudo tee -a /etc/hosts
echo "127.0.0.1   ${jellyfin_ingress_host} ${ingress_host}" | sudo tee -a /etc/hosts

wget --retry-on-http-error=503,500 "${ingress_host}/sonarr" || true
wget --retry-on-http-error=503,500 "${ingress_host}/radarr" || true
wget --retry-on-http-error=503,500 "${ingress_host}/sabnzbd" || true
wget --retry-on-http-error=503,500 "${ingress_host}/prowlarr" || true
wget --retry-on-http-error=503,500 "${ingress_host}/jackett" || true
