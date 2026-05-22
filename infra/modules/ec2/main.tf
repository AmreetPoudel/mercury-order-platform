resource "aws_instance" "ec2" {
  ami           = "ami-0388e3ada3d9812da" # 
  instance_type = "t3.micro"
  subnet_id = var.subnet_id
  vpc_security_group_ids=var.vpc_security_group_id
  iam_instance_profile = var.instance_profile_name
  associate_public_ip_address = true
  key_name = "mercury-key"
  user_data_replace_on_change = true
  user_data = file("${path.module}/user_data.sh")

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