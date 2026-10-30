# Cloud-Native Health Monitor

A production-grade, GitOps-driven microservice and platform repository demonstrating non-blocking asynchronous telemetry polling, hardened container security, modular Infrastructure as Code (IaC) on AWS EKS 1.35, and native Prometheus Operator observability.

---

## Architecture Overview

```mermaid
graph TD
    Dev[Platform Engineer] -->|git push origin main| GHA[GitHub Actions CI/CD]

    subgraph "CI & Security Pipeline"
        GHA -->|1. Test| Pytest[Pytest Async Test Suite]
        GHA -->|2. Scan| Trivy[Trivy Vulnerability Scanner]
        GHA -->|3. Authenticate| OIDC[AWS IAM OIDC Federation]
        GHA -->|4. Push Image| ECR[Amazon ECR / Docker Hub]
        GHA -->|5. Update values.yaml| GitOpsCommit[Automated Git SHA Commit - skip ci]
    end

    subgraph "Continuous Delivery & Cluster Runtime"
        GitOpsCommit -->|Syncs Declarative State| ArgoCD[Argo CD GitOps Controller]
        ArgoCD -->|Reconciles Helm Chart| Helm[Helm Engine]
        Helm -->|Deploys to Cluster| K8s[Amazon EKS 1.35 / Local Cluster]

        subgraph "Kubernetes Workloads & Observability"
            Ingress[NGINX Ingress] -->|Routes Traffic| Svc[ClusterIP Service: 8080]
            Svc --> Pod1[FastAPI Async Pod 1]
            Svc --> Pod2[FastAPI Async Pod 2]
            SM[ServiceMonitor] -->|Scrape Target /metrics| Prom[Prometheus Operator]
            Prom -->|Scrapes Metrics| Pod1
            Prom -->|Scrapes Metrics| Pod2
            Prom -->|Metrics Source| Grafana[Grafana Telemetry Dashboard]
        end
    end

    subgraph "Infrastructure as Code (Terraform)"
        TF[Terraform Modules] -->|Provisions| VPC[AWS VPC Dual-AZ + NAT Gateway]
        TF -->|Provisions| EKS[Amazon EKS 1.35 Cluster]
        TF -->|Remote State| S3[Encrypted S3 Bucket + Native S3 State Locking]
        TF -->|Configures| IRSA[IAM OIDC Provider for Pods]
    end
