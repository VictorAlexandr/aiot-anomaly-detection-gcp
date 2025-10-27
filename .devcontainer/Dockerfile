# .devcontainer/Dockerfile

# Começamos com a mesma imagem base de Python
FROM mcr.microsoft.com/devcontainers/python:3.10

# Executamos tudo como root para garantir as permissões de instalação
USER root

# --- Instala o Google Cloud SDK (Método Atualizado) ---
RUN apt-get update && apt-get install -y curl gnupg apt-transport-https ca-certificates && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    apt-get update -y && apt-get install -y google-cloud-sdk

# --- Instala o Terraform ---
RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip && \
    unzip terraform_1.5.7_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_1.5.7_linux_amd64.zip

# Voltamos ao usuário padrão do container
USER vscode