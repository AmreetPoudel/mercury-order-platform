resource "aws_security_group" "mercury_sg" {
  name        = "mercury-api-sg"
  description = "Allow API and SSH access"
  vpc_id      = var.vpc_id

  tags = {
    Name = "mercury-api-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_api_ipv4" {
  security_group_id = aws_security_group.mercury_sg.id

  cidr_ipv4 = "0.0.0.0/0"

  from_port = 8000
  to_port   = 8000

  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "allow_ssh_ipv4" {
  security_group_id = aws_security_group.mercury_sg.id

  cidr_ipv4 = "0.0.0.0/0"

  from_port = 22
  to_port   = 22

  ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4" {
  security_group_id = aws_security_group.mercury_sg.id

  cidr_ipv4 = "0.0.0.0/0"

  ip_protocol = "-1"
}