variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "eu-central-1"
}

variable "github_repo" {
  description = "GitHub repository formatted as owner/repo"
  type        = string
  default     = "amzmohamed/cloud-native-health-monitor"
}
