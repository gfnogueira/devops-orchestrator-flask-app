# devops-orchestrator-flask-app

A Flask application designed for DevOps orchestration, monitoring, and demonstration purposes. This project includes:

- Health and readiness endpoints for Kubernetes probes
- Prometheus metrics integration for observability
- Sample API endpoint for demonstration
- Logging setup for application events
- Helm chart for Kubernetes deployment
- Example tests for API endpoints

## Features

- **Health Check**: `/health` endpoint for liveness probes
- **Readiness Check**: `/ready` endpoint for readiness probes
- **Metrics**: `/metrics` endpoint exposes Prometheus metrics
- **Sample Data API**: `/api/data` returns sample data
- **Logging**: Application logs important events
- **Error Handling**: Custom handlers for 404 and 500 errors

## Getting Started

### Prerequisites
- Python 3.8+
- Docker (optional, for containerization)
- Helm (for Kubernetes deployment)

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/gfnogueira/devops-orchestrator-flask-app.git
   cd devops-orchestrator-flask-app
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Running Locally
```sh
python app/app.py
```

Or with Docker:
```sh
docker build -t devops-orchestrator-flask-app .
docker run -p 5000:5000 devops-orchestrator-flask-app
```

### Kubernetes Deployment
1. Update values in `charts/values.yaml` as needed.
2. Deploy with Helm:
   ```sh
   helm install devops-orchestrator ./charts
   ```

## Endpoints
- `/` - Welcome message
- `/health` - Health check
- `/ready` - Readiness check
- `/metrics` - Prometheus metrics
- `/api/data` - Sample data

## Testing
Run tests with:
```sh
pytest tests/
```
