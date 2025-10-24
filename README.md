# AIoT Anomaly Detection Pipeline on GCP

## 1. Visão Geral do Projeto

Este projeto implementa um pipeline de MLOps de ponta a ponta para detecção de anomalias em dados de séries temporais, simulando um cenário real de AIoT (Inteligência Artificial das Coisas). O sistema ingere dados de sensores, utiliza um modelo de Deep Learning (LSTM Autoencoder) para identificar padrões anômalos (como vazamentos ou fraudes) e expõe as previsões através de uma API RESTful.

Toda a infraestrutura é provisionada e gerenciada no Google Cloud Platform (GCP) utilizando práticas de Infraestrutura como Código (IaC) com Terraform e automação de CI/CD com GitHub Actions.

## 2. Objetivos

*   **Técnicos:**
    *   Construir um pipeline robusto e automatizado na GCP.
    *   Implementar um modelo de detecção de anomalias com LSTM Autoencoder.
    *   Containerizar a aplicação de inferência com Docker.
    *   Expor o modelo como um serviço escalável usando FastAPI e Cloud Run.
    *   Automatizar o provisionamento da infraestrutura com Terraform.
    *   Criar um pipeline de CI/CD para build e deploy contínuos.
*   **De Portfólio:**
    *   Demonstrar proficiência em MLOps, DevOps, arquitetura de nuvem e Deep Learning.
    *   Criar um projeto complexo e bem documentado que simula desafios do mundo real.

## 3. Métricas de Sucesso

*   **Funcionalidade:** O pipeline processa dados e a API retorna predições de anomalia corretamente.
*   **Automação:** A infraestrutura pode ser provisionada com um único comando (`terraform apply`).
*   **CI/CD:** Novas alterações no código na branch `main` acionam um build e deploy automáticos com sucesso.
*   **Performance:** A API de inferência responde a requisições em menos de 500ms sob carga de teste.

## 4. Arquitetura do Sistema

O fluxo de dados e operações segue a seguinte arquitetura:

![Arquitetura AIoT Anomaly Detection](link_para_sua_imagem_da_arquitetura.png)  <!-- Você pode adicionar a imagem depois -->

1.  **Ingestão de Dados:** Um script simulador envia dados de sensores (em formato JSON) para um tópico no **GCP Pub/Sub**.
2.  **Processamento:** Uma **Cloud Function** é acionada por novas mensagens no tópico, realizando o pré-processamento necessário nos dados.
3.  **API de Inferência:** A aplicação FastAPI, containerizada com Docker, é executada no **Cloud Run**. Ela carrega o modelo treinado de LSTM Autoencoder.
4.  **Predição:** A API recebe os dados pré-processados, realiza a inferência e retorna se o dado recebido constitui uma anomalia.
5.  **CI/CD - Automação:**
    *   O código é versionado no **GitHub**.
    *   Quando há um push na branch `main`, o **GitHub Actions** é acionado.
    *   O **Cloud Build** constrói a imagem Docker.
    *   A nova imagem é enviada para o **Artifact Registry**.
    *   Finalmente, o **Cloud Run** é atualizado para servir a nova versão da aplicação.
6.  **IaC - Infraestrutura:** Todos os recursos da GCP (Pub/Sub, Cloud Run, etc.) são definidos e gerenciados via código **Terraform**.
## 5. Stack de Tecnologias

*   **Linguagem:** Python
*   **Modelagem:** TensorFlow, Pandas, Scikit-learn
*   **API:** FastAPI
*   **Containerização:** Docker
*   **Nuvem:** Google Cloud Platform (Cloud Run, Cloud Build, Artifact Registry, Pub/Sub, Cloud Functions)
*   **IaC & CI/CD:** Terraform, GitHub Actions
