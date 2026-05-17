module "vpc" {
  source = "../../modules/vpc"

  vpc_cidr           = "10.0.0.0/16"
  public_subnet_cidr = "10.0.1.0/24"
  availability_zone  = "ap-south-1a"
}

module "sg" {
  source = "../../modules/sg"
  vpc_id = module.vpc.vpc_id
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



module "ec2" {
  source = "../../modules/ec2"
  subnet_id = module.vpc.public_subnet_id
  vpc_security_group_ids = [module.sg.sg_id]
}