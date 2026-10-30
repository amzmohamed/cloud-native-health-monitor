terraform {
  backend "s3" {
    bucket       = "cloud-native-health-monitor-tfstate"
    key          = "dev/terraform.tfstate"
    region       = "eu-central-1"
    use_lockfile = true
    encrypt      = true
  }
}
