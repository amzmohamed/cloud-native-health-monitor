# Cloud-Native Health Monitor Microservice

[![CI/CD Pipeline](https://github.com/amzmohamed/cloud-native-health-monitor/actions/workflows/ci-cd.yaml/badge.svg)](https://github.com/amzmohamed/cloud-native-health-monitor/actions)
![Docker](https://img.shields.io/badge/docker-multi--stage-blue)
![Kubernetes](https://img.shields.io/badge/kubernetes-declarative-326CE5)
![Prometheus](https://img.shields.io/badge/metrics-prometheus-E6522C)
![Python](https://img.shields.io/badge/python-3.11-3776AB)

A lightweight, production-grade telemetry microservice built in Python (FastAPI) that continuously monitors external JSON and XML API endpoints, validates data contracts and payload schemas, and exposes standard Prometheus metrics for SLA and reliability monitoring.

---

## Architecture Overview

```text
                        +----------------------------+
                        |  Kubernetes Cluster        |
                        |                            |
  Incoming Traffic ---> |  Ingress (monitor.local)   |
                        +--------------+-------------+
                                       |
                                       v
                        +--------------+-------------+
                        |  ClusterIP Service (:8080) |
                        +--------------+-------------+
                                       |
                                       v
                        +----------------------------+
                        |  Deployment (2 Replicas)   |
                        |  - Non-root user (10001)   |
                        |  - ConfigMap driven        |
                        |  - Health Probes (L/R)     |
                        +--------------+-------------+
                                       |
                  +--------------------+--------------------+
                  |                                         |
                  v                                         v
       +--------------------+                    +--------------------+
       |  Target JSON API   |                    |  Target XML API    |
       +--------------------+                    +--------------------+
```

---

## Core Features

* **Multi-Format Ingestion:** Actively polls and validates both JSON payloads and XML schemas using secure parsers (`defusedxml`).
* **Prometheus Metrics Exporter:** Exposes operational telemetry at `/metrics`, including endpoint availability (`endpoint_up`), request latency (`endpoint_latency_seconds`), and categorized schema validation failures (`endpoint_validation_failures_total`).
* **Hardened Multi-Stage Container:** Built on `python:3.11-slim` using multi-stage compilation and executed under an unprivileged, non-root user (`UID 10001`).
* **Production Kubernetes Manifests:** Complete declarative configurations with resource constraints (`limits`/`requests`), ConfigMap environment decoupling, liveness/readiness probes, and Ingress routing.
* **Automated CI/CD:** GitHub Actions workflow executing automated `pytest` suites, Trivy container security vulnerability scanning, and multi-architecture Docker Hub publishing.

---

## Endpoints

| Path | Method | Purpose |
| :--- | :--- | :--- |
| `/healthz` | GET | Liveness probe returning application runtime status |
| `/ready` | GET | Readiness probe for upstream traffic routing |
| `/metrics` | GET | Prometheus telemetry scrape endpoint |

---

## Quickstart

### Local Development
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r app/requirements.txt
pytest tests/ -v
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Docker Execution
```bash
docker build -t cloud-native-health-monitor:latest .
docker run -d -p 8080:8080 --name health-monitor cloud-native-health-monitor:latest
curl http://localhost:8080/healthz
curl http://localhost:8080/metrics
```

### Kubernetes Deployment
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```