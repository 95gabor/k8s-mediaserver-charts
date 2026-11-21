{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "sonarr.name" -}}
{{- default .Chart.Name | trunc 63 }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "sonarr.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "sonarr.labels" -}}
helm.sh/chart: {{ include "sonarr.chart" . }}
{{ include "sonarr.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "sonarr.selectorLabels" -}}
app.kubernetes.io/name: {{ include "sonarr.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Path of the downloads folder inside the container. With unifiedMount the whole volume is
mounted once, so downloads and the library share a mount point and hardlinks work.
*/}}
{{- define "sonarr.downloadsPath" -}}
{{- if .Values.general.storage.unifiedMount.enabled -}}
{{- printf "%s/%s" (.Values.general.storage.unifiedMount.path | trimSuffix "/") .Values.general.storage.subPaths.downloads -}}
{{- else -}}
/downloads
{{- end -}}
{{- end }}

{{/*
Path of the tv library inside the container (see downloadsPath).
*/}}
{{- define "sonarr.libraryPath" -}}
{{- if .Values.general.storage.unifiedMount.enabled -}}
{{- printf "%s/%s" (.Values.general.storage.unifiedMount.path | trimSuffix "/") .Values.general.storage.subPaths.tv -}}
{{- else -}}
/tv
{{- end -}}
{{- end }}
