resource "aws_iam_role" "ec2_role" {
  name = "mercury-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}


resource "aws_iam_policy" "ssm_read" {
  name = "mercury-ssm-read"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]

        Resource = "*"
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "ssm_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.ssm_read.arn
}


resource "aws_iam_instance_profile" "ec2_profile" {
  name = "mercury-ec2-profile"

  role = aws_iam_role.ec2_role.name
}