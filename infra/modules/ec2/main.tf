resource "aws_instance" "ec2" {
  ami           = "ami-005e54dee72cc1d00" # 
  instance_type = "t2.micro"

  primary_network_interface {
    network_interface_id = aws_network_interface.example.id
  }

  credit_specification {
    cpu_credits = "unlimited"
  }
}