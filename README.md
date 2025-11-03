# app-2024mt03611

A simple app is created using Flask, built using docker, deployed on kuberentes and monitored via prometheus with cadvisor enabled

# DevOps Assignment - Flask Application Deployment

## Table of Contents
1. [Task 1: Create the Backend Application using Flask](#task-1-create-the-backend-application-using-flask)
2. [Task 2: Dockerize the Backend Application](#task-2-dockerize-the-backend-application)
3. [Task 3: Run the Docker Container](#task-3-run-the-docker-container)
4. [Task 4: Deploy the Docker Image to a Kubernetes Cluster](#task-4-deploy-the-docker-image-to-a-kubernetes-cluster)
5. [Task 5: Configure Networking with a Load Balancer](#task-5-configure-networking-with-a-load-balancer)
6. [Task 6: Configure Prometheus for Metrics Collection](#task-6-setting-up-prometheus-monitoring)

## Task 1: Create the Backend Application using Flask

### Project Structure
- `main.py` - Flask application with ASGI support
- `requirements.txt` - Python dependencies
- `.env` - Environment variables configuration

### Setup and Installation

1. Create virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Configuration
Environment variables in `.env`:
```
APP_VERSION=1.0
APP_TITLE="Devops for Cloud Assignment"
```


### Running the Application
```powershell
python -m uvicorn main:asgi_app --reload --host 127.0.0.1 --port 8000
```

### API Endpoints
1. Root endpoint (`/`):
```json
{
    "message": "Welcome to the DevOps Application",
    "author": "Aditya Jambhalikar - 2024MT03611",
    "status": "running",
    "available_endpoints": {
        "/": "Get this information",
        "/get_info": "Get application version and title"
    }
}
```

2. Info endpoint (`/get_info`):
```json
{
    "APP_VERSION": "1.0",
    "APP_TITLE": "Devops for Cloud Assignment"
}
```

## Task 2: Dockerize the Backend Application

### Prerequisites
- Docker installed and running

### Dockerfile Configuration
Created `Dockerfile` with:
- Base image: python:3.11-slim
- Working directory: /app
- Dependencies installation
- Environment variables configuration
- Port exposure: 8000d

### Building the Image
```bash
docker build -t img-2024mt03611 .
```

## Task 3: Run the Docker Container

### Running Container
```bash
docker run --name cnr-2024mt03611 -p 8000:8000 img-2024mt03611
```

### Verification
Access endpoints at:
- http://localhost:8000/
- http://localhost:8000/get_info

## Task 4: Deploy the Docker Image to a Kubernetes Cluster

### Prerequisites
- Kubernetes cluster running
- kubectl configured

### Deployment Steps
1. Apply ConfigMap:
```bash
kubectl apply -f config-2024MT03611.yaml
```

2. Create deployment:
```bash
kubectl apply -f dep-2024MT03611.yaml
```

3. Verify deployment:
```bash
kubectl get pods -l app=flask-app-2024mt03611
kubectl get deployment dep-2024mt03611
```

## Task 5: Configure Networking with a Load Balancer

### Load Balancer Setup
1. Create service (`svc-2024MT03611.yaml`):
```bash
kubectl apply -f svc-2024MT03611.yaml
```

2. Verify service creation:
```bash
kubectl get service svc-2024mt03611
```

### Testing Load Balancing
1. Get Load Balancer IP:
```bash
kubectl get service svc-2024mt03611 -o wide
```

### Monitoring Request Distribution
1. View pod logs:
```bash
# Get pod names
kubectl get pods -l app=flask-app-2024mt03611

# Check logs for each pod
kubectl logs <pod-name-1>
kubectl logs <pod-name-2>

# Full logs
kubectl logs -f -l app=flask-app-2024mt03611
```

### Verification and Troubleshooting
Visit http://<external_ip>/get_info
In case of Docker Desktop, localhost will be external ip so visit 
http://localhost/get_info

## Task 6: Setting up Prometheus Monitoring

### Prerequisites
- Kubernetes cluster with RBAC enabled
- kubectl configured

### Setup Steps

1. Create Prometheus Service Account and RBAC:
```bash
kubectl apply -f service-account-prometheus.yaml
```

2. Create Prometheus ConfigMap:
```bash
kubectl apply -f config-prometheus.yaml
```

3. Deploy Prometheus:
```bash
kubectl apply -f dep-prometheus.yaml
```

### Accessing Prometheus UI

1. Get the NodePort for Prometheus service:
```bash
kubectl get svc prometheus-service
```

2. Access Prometheus UI at:
- If using Docker Desktop: http://localhost:<nodePort>
- If using remote cluster: http://<node-ip>:<nodePort>

### Available Metrics

1. Application Metrics:
- `get_info_requests_total`: Counter for /get_info endpoint requests

2. Container Resource Metrics:
- CPU Usage Query:
```
sum(rate(container_cpu_usage_seconds_total{pod=~"dep-2024mt03611-.*"}[5m])) by (pod)
```

- Memory Usage Query (in MB):
```
sum(container_memory_working_set_bytes{pod=~"dep-2024mt03611-.*"}) by (pod) / 1024 / 1024
```

### Monitoring Configuration
- Prometheus scrapes metrics every 15 seconds
- Configured to monitor:
  - Flask application endpoints
  - Kubernetes cAdvisor metrics
  - Prometheus itself

