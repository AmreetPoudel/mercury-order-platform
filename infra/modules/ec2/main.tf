resource "aws_instance" "ec2" {
  ami           = "ami-0388e3ada3d9812da" # 
  instance_type = "t3.micro"
  subnet_id = var.subnet_id
  vpc_security_group_ids=var.vpc_security_group_ids

  associate_public_ip_address = true
  key_name = "mercury-key"

  tags = {
    Name = "mercury-platform-ec2"
  }

  }


resource "aws_eip" "mercury_eip" {
  instance = aws_instance.ec2.id

  tags = {
    Name = "mercury-eip"
  }
}