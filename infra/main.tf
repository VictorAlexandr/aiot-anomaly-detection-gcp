# infra/main.tf (VERSÃO COMPLETA E CORRIGIDA)

# --- RECURSOS DE INGESTÃO DE DADOS ---

resource "google_pubsub_topic" "sensor_data" {
  project = var.gcp_project_id
  name    = "aiot-sensor-data"
}

resource "google_storage_bucket" "function_source_code" {
  project                     = var.gcp_project_id
  name                        = "${var.gcp_project_id}-cf-source"
  location                    = var.gcp_region
  uniform_bucket_level_access = true
}

data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = "../src/cloud_functions/data_processor/"
  output_path = "/tmp/data_processor.zip"
}

resource "google_storage_bucket_object" "function_source_zip" {
  name   = "source.zip#${data.archive_file.function_source.output_md5}"
  bucket = google_storage_bucket.function_source_code.name
  source = data.archive_file.function_source.output_path
}

resource "google_cloudfunctions_function" "data_processor_function" {
  // API da Cloud Function exige o NOME do projeto
  project = var.gcp_project_name

  region              = var.gcp_region
  name                = "aiot-data-processor"
  runtime             = "python310"
  available_memory_mb = 256

  source_archive_bucket = google_storage_bucket.function_source_code.name
  source_archive_object = google_storage_bucket_object.function_source_zip.name
  entry_point           = "process_sensor_data"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    // E o gatilho também exige o NOME do projeto
    resource = "projects/${var.gcp_project_name}/topics/${google_pubsub_topic.sensor_data.name}"
  }
}


# --- RECURSOS DA API DE INFERÊNCIA ---

resource "google_artifact_registry_repository" "api_images" {
  provider = google-beta
  // API do Artifact Registry exige o NOME do projeto
  project       = var.gcp_project_name
  location      = var.gcp_region
  repository_id = "aiot-anomaly-api-repo"
  description   = "Repositório para as imagens Docker da API de anomalia."
  format        = "DOCKER"
}

resource "google_cloud_run_v2_service" "api_service" {
  provider = google-beta
  project  = var.gcp_project_name
  name     = "aiot-anomaly-api"
  location = var.gcp_region

  deletion_protection = false
  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello" # Usaremos um placeholder por enquanto

      ports {
        container_port = 8000 # A porta que nossa API expõe
      }
    }
  }
}

# --- Políticas de IAM ---
resource "google_cloud_run_v2_service_iam_member" "allow_public_access" {
  provider = google-beta
  project  = var.gcp_project_name
  location = var.gcp_region
  name     = google_cloud_run_v2_service.api_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
