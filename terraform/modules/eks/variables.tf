variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "health-monitor-eks"
}

variable "cluster_version" {
  description = "Kubernetes version for EKS control plane"
  type        = string
  default     = "1.30"
}

variable "vpc_id" {
  description = "ID of the dedicated VPC"
  type        = string
}

variable "subnet_ids" {
  description = "Subnet IDs for control plane network interfaces and worker nodes"
  type        = list(string)
}

variable "instance_types" {
  description = "EC2 instance types for the worker nodes"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "desired_size" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2
}

variable "min_size" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 1
}

variable "max_size" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 3
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
