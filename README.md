# IRD Data Pipeline

## 🎯 Objective

The **IRD Data Pipeline** is an automated system designed to scrape, preprocess, and index tax-related data from the Inland Revenue Department (IRD) website. The primary goal is to build a high-quality knowledge base for a Retrieval-Augmented Generation (RAG) system, enabling efficient semantic search over IRD's public records and PDF documents.

The pipeline is orchestrated using **Prefect**, streamlining three core stages:

1. **Scrape Flow**: Extracts case data and downloads PDF documents.
2. **Preprocess Flow**: Converts PDFs to Markdown using **IBM Docling** (chosen for its superior table and layout preservation) and performs text cleansing.
3. **RAG Flow**: Indexes the processed data into a vector database (supporting **ChromaDB**, **OpenSearch**, or **AWS OpenSearch**) for semantic retrieval.

---

## 📂 Repository Structure

```text
ird_data_pipeline/
├── assets/                 # Project images and documentation assets
├── data/                   # Local storage for scraped PDFs and Markdown files
├── docker/                 # Docker configurations for the app and OpenSearch
├── docs/                   # Technical research and infrastructure guides
├── infra/                  # Terraform scripts for AWS infrastructure provisioning
├── lib/                    # Project dependencies (requirements.txt)
├── src/
│   ├── config/             # Configuration management and environment settings
│   ├── core/               # Core business logic
│   │   ├── preprocess/     # PDF-to-Markdown conversion and text cleansing
│   │   ├── process/        # RAG implementation and retrieval logic
│   │   ├── scrape/         # Scrapy spiders and PDF downloaders
│   │   └── vector_stores/  # Vector DB clients (Chroma, OpenSearch, AWS OpenSearch)
│   ├── initialize/         # System initialization and model loading
│   └── pipelines/          # Prefect flow definitions (Scrape, Preprocess, RAG)
├── tests/                  # Unit tests and experimental notebooks
├── prefect.yaml            # Prefect local deployment configuration
└── prefect_cloud.yaml      # Prefect Cloud deployment configuration
```

---

## ⚙️ Setup and Installation

### 1. Configuration

The project uses two primary configuration files located in `src/config/files/`:

- `original.yaml`: Uses raw Markdown files created by Docling.
- `preprocessed.yaml`: Uses cleansed Markdown files.

**Execution Modes:**

- **Full Pipeline**: Set `scrape_data: true`, `save_pickle: true`, `load_pickle: false`.
- **Load Cached Data**: Set `scrape_data: false`, `save_pickle: false`, `load_pickle: true` to use existing `.pkl` files.

### 2. Local Environment Setup

**Prerequisites:** Docker, Conda

1. **Start OpenSearch**:

   ```bash
   cd docker/opensearch
   docker-compose up -d
   ```
2. **Environment Variables**:
   Create a `.env` file based on `.env.template`.
3. **Python Environment**:

   ```bash
   conda create -n ird_rag python=3.11 -y
   conda activate ird_rag
   pip install --no-cache-dir -r ./lib/requirements.txt
   export PYTHONPATH=.
   ```
4. **Build Docker Image (Optional)**:

   ```bash
   docker build -f docker/Dockerfile -t ird_data_pipeline_scrape:0.0.1 .
   ```

---

## 🚀 Running the Pipeline

### Local Execution (Prefect Server)

1. **Start Prefect Server**:
   ```bash
   prefect server start
   ```
2. **Start Worker Pool**:
   ```bash
   prefect worker start --pool "ird-data-pool"
   ```
3. **Deploy and Run**:
   ```bash
   prefect deploy
   prefect deployment run 'ird_scrape_data_dag/ird-data-pipeline-deployment'
   ```

### Cloud Execution (Prefect Cloud)

1. **Configure Secrets**: Set required environment variables in the Prefect Cloud portal.
2. **Deploy to Cloud**:
   ```bash
   prefect deploy --prefect-file prefect_cloud.yaml
   ```

### ☁️ AWS OpenSearch Provisioning

For production-grade vector storage, the project includes Terraform scripts to provision an AWS OpenSearch cluster.

1. **Navigate to Terraform directory**:
   ```bash
   cd infra/terraform
   ```
2. **Initialize and Apply**:
   ```bash
   terraform init
   terraform plan -out=tfplan
   terraform apply tfplan
   ```
3. **Update Configuration**: Once provisioned, update your `.env` or Prefect Cloud secrets with the provided OpenSearch endpoint and credentials.

---

### 📺 Prefect Cloud Demo

![Prefect Cloud Pipeline Execution](assets/imgs/prefect_cloud_demo.gif)
*(Replace this placeholder with your actual GIF)*

---

## 🛠️ Tech Stack

- **Orchestration**: Prefect
- **PDF Parsing**: IBM Docling
- **Scraping**: Scrapy, Wget
- **RAG Framework**: LlamaIndex
- **Vector DB**: AWS OpenSearch / ChromaDB
- **Infrastructure**: Terraform, Docker
