# Network Security: MLOps-Driven Network Intrusion Detection System

An end-to-end, production-grade ML pipeline for automated network intrusion detection. By combining XGBoost classification, DVC versioning, MLflow experiment tracking (via DagshHub), and a FastAPI web interface, this system delivers accurate threat detection with full reproducibility and traceability—ready for deployment.

***

## 📂 Repository Structure

```
.
├── .dvc/                          # DVC configuration & cache
├── .github/workflows/             # CI/CD pipelines
├── config/                        # Project-wide YAML configuration
├── notebook/                      # Exploratory data analysis & experiments
├── schema/                        # Saved schema definitions (YAML)
├── src/
│   └── package/                   # Package source
│       ├── configuration.py       # Config dataclasses
│       ├── pipeline/              # Ingestion, validation, transformation, training, prediction
│       ├── components/            # Data ingestion, transformation, model training
│       ├── utils/                 # Model helpers, file I/O utilities
│       ├── logger.py              # Logging setup
│       ├── exception.py           # Custom exceptions
│       └── constants.py           # Project constants
├── templates/                     # Jinja2 templates for web UI
├── ETL.py                         # Orchestrates MongoDB ingestion, S3 push, schema save
├── dvc.yaml / dvc.lock            # Pipeline stage definitions & lock file
├── params.json                    # Pipeline hyperparameters
├── Dockerfile                     # Container image for deployment
├── app.py                         # FastAPI application entry point
├── main.py                        # Training pipeline orchestrator
├── service.py                     # Service configuration
├── requirements.txt               # Python dependencies
└── setup.py                       # Package installer
```


***

## 🔧 Core Workflow

### 1. Data Ingestion

Fetches network traffic data from MongoDB Atlas, converts to pandas DataFrame, validates schema against predefined YAML, and performs train-test split. Saves processed datasets locally and backs up to AWS S3.

### 2. Data Validation

Validates column schemas, missing values, and data types via `stage_02_data_validation.py`, ensuring data quality before transformation.

### 3. Data Transformation

Handles missing values, encodes categorical features, scales numerical data, and performs feature engineering in `stage_03_data_transformation.py`. Saves preprocessor pipeline as pickle for consistent inference.

### 4. Model Training

Trains and tunes XGBoost classifier through `stage_04_model_trainer.py`, logs metrics/artifacts to MLflow (hosted on DagshHub), and saves best model. Supports BentoML integration for serving.

### 5. Prediction Pipeline

* **Training Trigger**: GET `/train` endpoint invokes the full DVC→MLflow pipeline
* **Batch Prediction**: POST `/predict` accepts NumPy file upload, applies trained model + preprocessor, and displays results in HTML table
* **Deployment**: Exposed at `http://localhost:8000` via FastAPI with interactive docs at `/docs`

***

## ✅ Key Capabilities

* **Network Intrusion Detection**
Binary classification for detecting malicious network activities using traffic features (protocol types, service types, connection durations, byte counts, error rates).
* **Full MLOps Stack**
    - **DVC** for data \& artifact versioning
    - **MLflow** via DagshHub for experiment tracking \& model registry
    - **BentoML** for model serving and deployment
    - **Structured Logs \& Custom Exceptions** for robust pipeline observability
* **Interactive Prediction Interface**
FastAPI endpoint for batch predictions with HTML table visualization for security analysts.
* **Modular \& Extensible**
Clear separation of ingestion, validation, transformation, training, and inference; swap out model architectures or data sources with minimal changes.
* **Containerized Deployment**
Dockerfile for seamless local or cloud deployment with all dependencies packaged.

***

## 🛠️ Technology Stack

### Machine Learning \& MLOps

- **scikit-learn** - Data preprocessing, feature engineering, metrics
- **XGBoost** - Gradient boosting classifier
- **imbalanced-learn** - Handling class imbalance (SMOTE, etc.)
- **MLflow** - Experiment tracking \& model registry
- **DagshHub** - Hosted MLflow server \& data versioning
- **BentoML** - Model serving and packaging
- **DVC** - Data version control


### Backend \& API

- **FastAPI** - Async web framework
- **Uvicorn** - ASGI server
- **Jinja2** - Template rendering for HTML responses


### Data Processing

- **pandas** - Data manipulation
- **NumPy** - Numerical operations
- **PyYAML** - Configuration parsing
- **python-box** - Configuration management


### Database \& Storage

- **pymongo** - MongoDB Atlas client
- **boto3** - AWS S3 operations
- **certifi** - SSL certificate verification


### Development Tools

- **python-dotenv** - Environment variable management
- **ipykernel** - Jupyter notebook support

***

## 🚀 Deployment Architecture

### Cloud Infrastructure

- **Compute**: AWS EC2 instance (self-hosted GitHub runner)
- **Container Registry**: AWS Elastic Container Registry (ECR) for Docker images
- **Database**: MongoDB Atlas for network traffic data storage
- **Storage**: AWS S3 for artifact backups and data versioning
- **Experiment Tracking**: DagshHub (hosted MLflow server)


### CI/CD Pipeline

The `.github/workflows/main.yaml` automates testing, building, and deployment through three stages:

#### **Stage 1: Continuous Integration**

- **Runner**: `ubuntu-latest` (GitHub-hosted)
- **Steps**:
    - Checkout code from main branch
    - Lint repository
    - Run unit tests
- **Trigger**: Push to main branch (ignores README.md changes)


#### **Stage 2: Continuous Delivery (Build \& Push)**

- **Runner**: `ubuntu-latest` (GitHub-hosted)
- **Steps**:

1. Install utilities (`jq`, `unzip`)
2. Configure AWS credentials using GitHub Secrets
3. Login to Amazon ECR
4. Build Docker image from `Dockerfile`
5. Tag image as `latest`
6. Push to ECR repository
- **Dependencies**: Runs after integration stage passes


#### **Stage 3: Continuous Deployment**

- **Runner**: `self-hosted` (EC2 instance with GitHub Actions runner)
- **Steps**:

1. Configure AWS credentials
2. Login to Amazon ECR
3. Pull latest Docker image from ECR
4. Run container on EC2 instance:
        - Port mapping: `8080:8000` (host:container)
        - Environment variables: Loaded from `/home/ubuntu/.env`
        - Container name: `networksecurity`
        - IPC mode: `host` (for shared memory)
5. Clean up unused Docker resources (`docker system prune -af`)
- **Dependencies**: Runs after build-and-push stage completes


### GitHub Secrets Configuration

**Required secrets in GitHub repository settings:**

```bash
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1  # or your preferred region
ECR_REPOSITORY_NAME=network-security
AWS_ECR_LOGIN_URI=123456789012.dkr.ecr.us-east-1.amazonaws.com
```


### EC2 Instance Setup

**Prerequisites on EC2:**

1. **Docker Installation**: Docker engine installed and running
2. **GitHub Actions Runner**: Self-hosted runner configured and connected to repository
3. **AWS CLI**: Configured with ECR pull permissions
4. **Environment File**: `/home/ubuntu/.env` with application secrets:

```bash
URI=mongodb_atlas_connection_string
AWS_ACCESS_KEY_ID=aws_access_key
AWS_SECRET_ACCESS_KEY=aws_secret_key
S3_BUCKET=s3_bucket_name
MLFLOW_TRACKING_URI=https://dagshub.com/username/Network-Security.mlflow
DAGSHUB_TOKEN=dagshub_token
```

5. **Security Group**: Inbound rules allowing port 8080 (HTTP traffic)

### IAM Permissions

**ECR Permissions** (for GitHub Actions and EC2):

- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`
- `ecr:GetDownloadUrlForLayer`
- `ecr:BatchGetImage`
- `ecr:PutImage` (for push operations)
- `ecr:InitiateLayerUpload`
- `ecr:UploadLayerPart`
- `ecr:CompleteLayerUpload`

**S3 Permissions** (for artifact storage):

- `s3:PutObject`
- `s3:GetObject`
- `s3:ListBucket`


### Deployment Flow

```
Code Push (main branch)
         ↓
GitHub Actions (ubuntu-latest)
         ↓
    Integration Tests
         ↓
  Build Docker Image
         ↓
Push to AWS ECR (latest tag)
         ↓
Self-Hosted Runner (EC2)
         ↓
  Pull Image from ECR
         ↓
Run Container on EC2 (Port 8080)
         ↓
Application Live at http://<ec2-public-ip>:8080
```


***

## 🔄 Manual Deployment (Alternative)

If you need to deploy manually without CI/CD:

### 1. Build and Push to ECR

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t network-security:latest .

# Tag for ECR
docker tag network-security:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/network-security:latest

# Push to ECR
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/network-security:latest
```


### 2. Deploy on EC2

SSH into your EC2 instance:

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Pull latest image
docker pull 123456789012.dkr.ecr.us-east-1.amazonaws.com/network-security:latest

# Stop existing container (if running)
docker stop networksecurity && docker rm networksecurity

# Run new container
docker run -d -p 8080:8000 \
  --ipc="host" \
  --name=networksecurity \
  --env-file /home/ubuntu/.env \
  123456789012.dkr.ecr.us-east-1.amazonaws.com/network-security:latest

# Clean up unused resources
docker system prune -af
```


***

## 📦 Installation \& Setup

### Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)
- MongoDB Atlas account
- AWS account with S3 access
- DagshHub account for MLflow tracking


### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/hasan-raza-01/network-security.git
cd network-security
```

2. **Create virtual environment**
```bash
pip install --upgrade pip uv
uv venv .venv --python 3.9
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies**
```bash
uv pip install -e .
```

4. **Set up environment variables**
```bash
# Create .env file with following variables
URI=your_mongodb_atlas_connection_string
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
S3_BUCKET=your_s3_bucket_name
MLFLOW_TRACKING_URI=https://dagshub.com/your-username/Network-Security.mlflow
DAGSHUB_TOKEN=your_dagshub_token
```

5. **Run ETL Pipeline** (First-time data setup)
```bash
# Update data_path variable in ETL.py with local CSV path
uv run ETL.py
```

6. **Train the model**
```bash
# Option 1: Manual pipeline execution
uv run main.py

# Option 2: DVC pipeline (recommended)
dvc repro
```

7. **Run FastAPI server**
```bash
uv run app.py
```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

### Docker Setup

1. **Build Docker image**
```bash
docker build -t network-security:latest .
```

2. **Run container**
```bash
docker run -p 8000:8000 \
  --env-file .env \
  network-security:latest
```


***

## 🔄 CI/CD Pipeline \& Deployment

### GitHub Actions Workflow

The `.github/workflows/` automates:

1. **Test Stage**: Runs data validation and unit tests
2. **Train Stage**: Executes DVC pipeline for model training
3. **Build Stage**: Builds Docker image
4. **Deploy Stage**: Deploys to cloud platform (optional)

### Environment Variables for CI/CD

```bash
AWS_ACCESS_KEY_ID=aws_access_key
AWS_SECRET_ACCESS_KEY=aws_secret_key
AWS_ECR_LOGIN_URI=aws_uri_ECR
AWS_REGION=aws_region
ECR_REPOSITORY_NAME=ECR_repository_name
```


***

## 📋 API Endpoints

### Training

**GET** `/train`

Triggers the complete training pipeline (ingestion → validation → transformation → training).

**Response:**

```json
"Training is successful"
```


### Prediction

**POST** `/predict`

Accepts batch network traffic data for intrusion detection.

**Request:**

- File upload: NumPy array file (`.npy` format)
- Content-Type: `multipart/form-data`

**Response:**

- HTML table with predictions (0 = Normal, -1 = Intrusion)


### Health Check

**GET** `/`

Redirects to `/docs` for interactive API documentation.

***

## 📊 Model Performance

The XGBoost classifier achieves:

- **Accuracy**: ~95% on test set
- **Precision**: High true positive rate for intrusion detection
- **Recall**: Low false negative rate (critical for security applications)
- **F1-Score**: Balanced performance across classes

***

## 🔧 Configuration

### Pipeline Parameters

Edit `params.json` to customize model hyperparameters:

```json
{
  "xgb_classifier": {
    "n_estimators": 100,
    "learning_rate": 0.1,
    "max_depth": 6,
    "subsample": 0.8,
    "colsample_bytree": 0.8
  }
}
```


### DVC Pipeline

The `dvc.yaml` defines reproducible pipeline stages:

```yaml
stages:
  data_ingestion:
    cmd: python -m package.pipeline.training_pipeline
    deps:
      - ETL.py
    outs:
      - artifacts/data_ingestion/
  
  data_transformation:
    deps:
      - artifacts/data_ingestion/
    outs:
      - artifacts/data_transformation/
  
  model_training:
    deps:
      - artifacts/data_transformation/
    outs:
      - artifacts/model_trainer/
```


***

## 🔐 Security Best Practices

1. **Never commit credentials**: Use `.gitignore` for `.env` files
2. **Use environment variables**: Store sensitive config in environment
3. **MongoDB security**: Enable IP whitelisting and authentication
4. **S3 bucket policies**: Implement least-privilege access
5. **DagshHub tokens**: Rotate tokens periodically
6. **Container security**: Scan Docker images for vulnerabilities

***

## 📝 Development Status

This project is production-ready:

- ✅ Complete MLOps pipeline with DVC \& MLflow
- ✅ MongoDB Atlas integration for data ingestion
- ✅ AWS S3 backup and artifact storage
- ✅ DagshHub integration for experiment tracking
- ✅ FastAPI backend with batch prediction
- ✅ Docker containerization
- ✅ Comprehensive logging and error handling
- ✅ Schema validation and data quality checks

***

## 🐛 Troubleshooting

### MongoDB Connection Issues

**Problem**: `ServerSelectionTimeoutError`

**Solution**:

```bash
# Verify connection string format
URI=mongodb+srv://<username>:<password>@luster>.mongodb.net/<database>

# Check IP whitelist in MongoDB Atlas
# Ensure certifi is installed
pip install certifi
```


### DVC Pipeline Failures

**Problem**: `Stage failed with error`

**Solution**:

```bash
# Pull latest data
dvc pull

# Clear cache and repro
dvc repro --force

# Check status
dvc status
```


### Model Loading Errors

**Problem**: `BentoML model not found`

**Solution**:

```bash
# Check registered models
bentoml models list

# Fallback to pickle file
# The app automatically tries pickle if BentoML fails
```
