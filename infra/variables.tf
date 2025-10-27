# infra/variables.tf

variable "gcp_project_id" {
  description = "O ID numérico do projeto GCP."
  type        = string
}

variable "gcp_project_name" {
  description = "O nome literal (string ID) do projeto GCP."
  type        = string
}

variable "gcp_region" {
  description = "A região GCP padrão para os recursos."
  type        = string
  default     = "us-central1"
}