# infra/provider.tf

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.50.0"
    }
    # ADICIONE A DECLARAÇÃO DO PROVEDOR BETA
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 4.50.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# ADICIONE A CONFIGURAÇÃO DO PROVEDOR BETA
provider "google-beta" {
  project = var.gcp_project_id
  region  = var.gcp_region
}
