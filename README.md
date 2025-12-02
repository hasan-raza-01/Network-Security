# Network Security: MLOps-Driven Network Intrusion Detection System

An end-to-end, production-grade ML pipeline for automated network intrusion detection. By combining XGBoost classification, DVC versioning, MLflow experiment tracking (via DagshHub), and a FastAPI web interface, this system delivers accurate threat detection with full reproducibility and traceability—ready for deployment.

***

## 📂 Repository Structure

```
.
├── .dvc/                          # DVC configuration & cache for data version control
├── .github/
│   └── workflows/
│       └── main.yaml              # CI/CD pipeline: integration, build, and deployment automation
├── assets/                        # Static resources (images, diagrams)
├── config/
│   └── config.yaml                # Project-wide configuration: artifact paths, MongoDB settings, S3 bucket details
├── notebook/                      # Jupyter notebooks for EDA, experimentation, and prototyping
├── schema/                        # YAML schema definitions for data validation (column names, data types)
├── src/
│   └── package/                   # Main package source code
│       ├── __init__.py            # Package initializer
│       ├── cloud/
│       │   └── __init__.py        # AWS S3 operations: upload/download artifacts and data backups
│       ├── components/            # Core ML pipeline components
│       │   ├── __init__.py
│       │   ├── data_ingestion.py       # Fetches data from MongoDB, performs train-test split, saves to S3
│       │   ├── data_validation.py      # Validates schema, column names, data types, and missing values
│       │   ├── data_transformation.py  # Handles missing values, feature encoding, scaling, and preprocessing
│       │   ├── model_trainer.py        # Trains XGBoost classifier, logs metrics to MLflow, saves best model
│       │   └── prediction.py           # Loads trained model and preprocessor for batch predictions
│       ├── configuration/
│       │   └── mongo_db_connection.py # MongoDB Atlas connection handler with SSL certificate support
│       ├── constants/
│       │   └── __init__.py        # Project-level constants: file names, artifact paths, environment variables
│       ├── entity/
│       │   ├── __init__.py        # Dataclass entities for artifacts and configuration objects
│       │   ├── artifact_entity.py # Defines output artifacts for each pipeline stage
│       │   └── config_entity.py   # Configuration dataclasses for pipeline components
│       ├── exception/
│       │   └── __init__.py        # Custom exception handling with detailed error messages and tracebacks
│       ├── logger/
│       │   └── __init__.py        # Structured logging setup with timestamps and log rotation
│       ├── pipeline/              # Orchestration layer for training and prediction pipelines
│       │   ├── __init__.py
│       │   ├── stage_01_data_ingestion.py      # Orchestrates data ingestion component
│       │   ├── stage_02_data_validation.py     # Orchestrates data validation component
│       │   ├── stage_03_data_transformation.py # Orchestrates data transformation component
│       │   ├── stage_04_model_trainer.py       # Orchestrates model training component
│       │   ├── prediction_pipeline/
│       │   │   └── __init__.py    # Prediction pipeline: loads model and preprocessor for inference
│       │   └── training_pipeline/
│       │       └── __init__.py    # Training pipeline: executes all 4 stages sequentially
│       └── utils/
│           └── __init__.py        # Utility functions: file I/O (YAML, JSON, pickle), model loading/saving
├── templates/                     # Jinja2 HTML templates for web UI
│   ├── index.html                 # Upload interface for batch predictions
│   └── results.html               # Displays prediction results in tabular format
├── .dockerignore                  # Excludes unnecessary files from Docker image build
├── .dvcignore                     # Files ignored by DVC version control
├── .gitignore                     # Git exclusions: virtual environments, artifacts, secrets
├── Dockerfile                     # Multi-stage container image for production deployment
├── ETL.py                         # Orchestrates MongoDB → pandas → S3 pipeline and saves schema to YAML
├── app.py                         # FastAPI application: /train and /predict endpoints
├── dvc.lock                       # DVC lock file: ensures reproducibility with artifact hashes
├── dvc.yaml                       # DVC pipeline definition: stages, dependencies, and outputs
├── main.py                        # Training pipeline orchestrator: runs all 4 stages via DVC
├── params.json                    # Hyperparameters for XGBoost model (n_estimators, learning_rate, etc.)
├── requirements.txt               # Python dependencies: scikit-learn, XGBoost, FastAPI, DVC, MLflow, etc.
├── service.py                     # Service configuration: port settings, CORS, and app metadata
└── setup.py                       # Package installer: configures package for pip installation
```

### 📁 Directory & File Descriptions

#### **Root Configuration Files**
- **`.dockerignore`**: Specifies files excluded from Docker image builds (e.g., `.git`, `__pycache__`, `.env`) to reduce image size
- **`.dvcignore`**: Defines files DVC should ignore during version control operations
- **`.gitignore`**: Standard Git exclusions for Python projects (virtual environments, compiled files, secrets, artifacts)
- **`Dockerfile`**: Multi-stage build configuration for creating production-ready container images with Python dependencies
- **`dvc.yaml`**: Defines reproducible ML pipeline stages with dependencies and outputs tracked by DVC
- **`dvc.lock`**: Locks artifact versions with MD5 hashes to ensure exact reproducibility across environments
- **`params.json`**: Centralized hyperparameter configuration for XGBoost model tuning
- **`requirements.txt`**: Python package dependencies with versions for consistent environment setup
- **`setup.py`**: Package metadata and installation configuration for pip/setuptools

#### **Application Entry Points**
- **`ETL.py`**: Data ingestion script that pulls network traffic data from MongoDB Atlas, converts to pandas DataFrame, saves to local storage and S3, and generates schema YAML for validation
- **`app.py`**: FastAPI web application serving two endpoints:
  - `GET /train`: Triggers complete training pipeline
  - `POST /predict`: Accepts NumPy file upload for batch intrusion detection
- **`main.py`**: Manual training pipeline executor that sequentially runs all 4 stages (ingestion → validation → transformation → training)
- **`service.py`**: Application service configuration including port settings, CORS policies, and API metadata

#### **`.github/workflows/`**
- **`main.yaml`**: GitHub Actions CI/CD pipeline with three stages:
  1. **Integration**: Linting and unit tests on ubuntu-latest runner
  2. **Build & Push**: Docker image creation and push to AWS ECR
  3. **Deployment**: Pulls image and runs container on self-hosted EC2 runner

#### **`config/`**
- **`config.yaml`**: Project-wide YAML configuration containing:
  - Artifact directory paths for each pipeline stage
  - MongoDB database and collection names
  - AWS S3 bucket configuration
  - File naming conventions

#### **`schema/`**
Contains YAML schema files generated by `ETL.py` that define:
- Expected column names for validation
- Data types for each feature
- Categorical vs numerical feature lists

#### **`src/package/components/`**
Core ML pipeline components implementing business logic:
- **`data_ingestion.py`**: MongoDB Atlas data fetching, train-test split (80/20), and S3 backup operations
- **`data_validation.py`**: Schema validation against saved YAML, missing value checks, data type verification
- **`data_transformation.py`**: Handles missing values with KNN imputer, one-hot encoding for categorical features, robust scaling for numerical features, and saves preprocessing pipeline as pickle
- **`model_trainer.py`**: XGBoost classifier training with hyperparameter tuning, MLflow experiment tracking (metrics, parameters, artifacts), and BentoML model packaging for serving
- **`prediction.py`**: Loads trained model and preprocessor, applies transformations, and returns binary predictions (0=Normal, -1=Intrusion)

#### **`src/package/pipeline/`**
Orchestration layer that coordinates components:
- **`stage_01_data_ingestion.py`**: Reads config, initializes DataIngestion component, executes ingestion
- **`stage_02_data_validation.py`**: Validates ingested data against schema definitions
- **`stage_03_data_transformation.py`**: Applies preprocessing transformations and saves artifacts
- **`stage_04_model_trainer.py`**: Trains model, logs to MLflow, and saves best performer
- **`training_pipeline/__init__.py`**: Sequential pipeline executor running all 4 stages with error handling
- **`prediction_pipeline/__init__.py`**: Inference pipeline loading model/preprocessor and processing input data

#### **`src/package/cloud/`**
- **`__init__.py`**: S3Operations class for AWS interactions:
  - `sync_folder_to_s3()`: Uploads local artifacts to S3 bucket
  - `sync_folder_from_s3()`: Downloads artifacts from S3 for model serving

#### **`src/package/utils/`**
- **`__init__.py`**: Utility functions for file operations:
  - `read_yaml()`: Loads YAML configuration files
  - `write_yaml()`: Saves schema and config to YAML
  - `save_object()`: Serializes Python objects (models, preprocessors) as pickle
  - `load_object()`: Deserializes pickle files for inference
  - `save_numpy_array_data()` / `load_numpy_array_data()`: NumPy array I/O operations

#### **`src/package/configuration/`**
- **`mongo_db_connection.py`**: MongoDB Atlas connection manager:
  - Handles SSL certificate validation with certifi
  - Establishes PyMongo client with connection string from environment variables
  - Provides database and collection accessors

#### **`src/package/entity/`**
- **`artifact_entity.py`**: Dataclasses defining outputs from each pipeline stage:
  - `DataIngestionArtifact`: Train/test file paths
  - `DataValidationArtifact`: Validation status and report path
  - `DataTransformationArtifact`: Transformed data paths and preprocessor file
  - `ModelTrainerArtifact`: Trained model path and performance metrics
- **`config_entity.py`**: Configuration dataclasses for each component:
  - `DataIngestionConfig`: MongoDB settings, output paths
  - `DataValidationConfig`: Schema file path, validation thresholds
  - `DataTransformationConfig`: Preprocessor settings, output paths
  - `ModelTrainerConfig`: Model hyperparameters, MLflow settings

#### **`src/package/constants/`**
- **`__init__.py`**: Project-wide constants:
  - Environment variable names (e.g., `MONGODB_URI`, `AWS_ACCESS_KEY_ID`)
  - Artifact directory structure (e.g., `artifacts/data_ingestion/`)
  - File naming conventions (e.g., `train.csv`, `test.csv`, `model.pkl`)
  - S3 bucket names and paths

#### **`src/package/exception/`**
- **`__init__.py`**: Custom exception class `NetworkSecurityException`:
  - Captures detailed error messages with file name, line number, and traceback
  - Integrates with logger for comprehensive error tracking
  - Provides user-friendly error messages for debugging

#### **`src/package/logger/`**
- **`__init__.py`**: Logging configuration:
  - Creates timestamped log files in `logs/` directory
  - Formats logs with timestamp, log level, module name, and message
  - Supports both file and console output
  - Implements log rotation to prevent disk space issues

#### **`templates/`**
Jinja2 HTML templates for FastAPI web interface:
- **`index.html`**: File upload form for batch prediction (accepts `.npy` files)
- **`results.html`**: Displays prediction results in HTML table with color-coded threat levels

#### **`notebook/`**
Jupyter notebooks for:
- Exploratory Data Analysis (EDA) on network traffic data
- Feature importance analysis
- Model experimentation and hyperparameter tuning
- Visualizations of class distributions and feature correlations

#### **`assets/`**
Static resources including:
- Architecture diagrams (system design, data flow)
- Screenshots for documentation
- Sample prediction outputs

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