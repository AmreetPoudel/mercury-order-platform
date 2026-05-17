resource "aws_instance" "ec2" {
  ami           = "ami-0388e3ada3d9812da" # 
  instance_type = "t3.micro"
  subnet_id = var.subnet_id
  vpc_security_group_ids=var.vpc_security_group_ids

  associate_public_ip_address = true

  tags = {
    Name = "mercury-platform-ec2"
  }

  }