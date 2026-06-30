#!/usr/bin/env bash
set -euo pipefail

namespace="${1:-mediaserver}"
initial_sleep="${INITIAL_SLEEP:-15}"
final_sleep="${FINAL_SLEEP:-30}"

sleep "${initial_sleep}"

for pod in $(kubectl get pods -n "${namespace}" | awk 'NR>1{ print $1 }'); do
  while [[ $(kubectl get pods "${pod}" -n "${namespace}" -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do
    echo "Waiting for ${namespace} pods to be ready"
    sleep 10
  done
done

sleep "${final_sleep}"
