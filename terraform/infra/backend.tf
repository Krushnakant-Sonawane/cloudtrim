terraform {
  required_version = ">= 1.10"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket       = "cloudtrim-tfstate-975769100988"
    key          = "cloudtrim/infra.tfstate"
    region       = "ap-southeast-2"
    encrypt      = true
    use_lockfile = true # S3 native locking, no DynamoDB table needed
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Project   = "cloudtrim"
      ManagedBy = "terraform"
    }
  }
}
