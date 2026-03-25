terraform {
  required_version = ">= terraform_1.14.8"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> v6.37.0"
    }
  }
}