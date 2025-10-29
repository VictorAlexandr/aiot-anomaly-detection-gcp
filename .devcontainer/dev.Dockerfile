# .devcontainer/dev.Dockerfile (Versão Completa Final)

FROM mcr.microsoft.com/devcontainers/python:3.10

USER root

# --- Instala o Google Cloud SDK ---
RUN apt-get update && apt-get install -y curl gnupg apt-transport-https ca-certificates && \
  echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee /etc/apt/sources.list.d/google-cloud-sdk.list && \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
  apt-get update -y && apt-get install -y google-cloud-sdk

# --- Configura o Repositório do Docker e Instala as Ferramentas ---
RUN apt-get update && \
  # 1. Instala pré-requisitos para adicionar um novo repositório
  apt-get install -y ca-certificates curl && \
  install -m 0755 -d /etc/apt/keyrings && \
  # 2. Adiciona a chave GPG oficial do Docker
  curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
  chmod a+r /etc/apt/keyrings/docker.asc && \
  # 3. Adiciona o repositório do Docker às fontes do apt
  echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null && \
  apt-get update && \
  # 4. Agora instala o docker-ce-cli junto com as outras ferramentas
  apt-get install -y wget unzip git-lfs docker-ce-cli && \
  # 5. Continua com a instalação do Terraform
  wget https://releases.hashicorp.com/terraform/1.5.7/terraform_1.5.7_linux_amd64.zip && \
  unzip terraform_1.5.7_linux_amd64.zip && \
  mv terraform /usr/local/bin/ && \
  rm terraform_1.5.7_linux_amd64.zip && \
  git lfs install

# --- Configura Permissões do Docker ---
# Adiciona o usuário 'vscode' ao grupo 'docker' para permitir o uso do Docker CLI sem 'sudo'
# O comando pode retornar um erro inofensivo se o grupo já existir.
RUN groupadd docker || true && usermod -aG docker vscode

# Voltamos ao usuário padrão do container
USER vscode