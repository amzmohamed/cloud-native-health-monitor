terraform {
  backend "s3" {
    bucket         = "cloud-native-health-monitor-tfstate"
    key            = "dev/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
