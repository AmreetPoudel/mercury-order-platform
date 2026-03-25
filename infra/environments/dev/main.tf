module "vpc" {
  source = "../../modules/vpc"
}

module "sg" {
  source = "../../modules/sg"
}

module "iam" {
  source = "../../modules/iam"
}

module "s3" {
  source = "../../modules/s3"
}

module "ecr" {
  source = "../../modules/ecr"
}

module "sqs" {
  source = "../../modules/sqs"
}