{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "radarr.name" -}}
{{- default .Chart.Name | trunc 63 }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "radarr.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "radarr.labels" -}}
helm.sh/chart: {{ include "radarr.chart" . }}
{{ include "radarr.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "radarr.selectorLabels" -}}
app.kubernetes.io/name: {{ include "radarr.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Path of the downloads folder inside the container. With unifiedMount the whole volume is
mounted once, so downloads and the library share a mount point and hardlinks work.
*/}}
{{- define "radarr.downloadsPath" -}}
{{- if .Values.general.storage.unifiedMount.enabled -}}
{{- printf "%s/%s" (.Values.general.storage.unifiedMount.path | trimSuffix "/") .Values.general.storage.subPaths.downloads -}}
{{- else -}}
/downloads
{{- end -}}
{{- end }}

{{/*
Path of the movies library inside the container (see downloadsPath).
*/}}
{{- define "radarr.libraryPath" -}}
{{- if .Values.general.storage.unifiedMount.enabled -}}
{{- printf "%s/%s" (.Values.general.storage.unifiedMount.path | trimSuffix "/") .Values.general.storage.subPaths.movies -}}
{{- else -}}
/movies
{{- end -}}
{{- end }}
