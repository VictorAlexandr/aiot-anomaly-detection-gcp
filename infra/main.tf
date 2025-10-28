# infra/main.tf (VERSÃO FINAL CORRIGIDA)

resource "google_pubsub_topic" "sensor_data" {
  project = var.gcp_project_id
  name    = "aiot-sensor-data" # Nome correto do tópico
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
  // Usa o NOME STRING do projeto
  project = var.gcp_project_name

  region = var.gcp_region
  // Nome correto da função
  name    = "aiot-data-processor"
  runtime = "python310"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.function_source_code.name
  source_archive_object = google_storage_bucket_object.function_source_zip.name
  entry_point           = "process_sensor_data"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    // Constrói o gatilho com o NOME STRING do projeto e o NOME do tópico
    resource = "projects/${var.gcp_project_name}/topics/${google_pubsub_topic.sensor_data.name}"
  }
}
