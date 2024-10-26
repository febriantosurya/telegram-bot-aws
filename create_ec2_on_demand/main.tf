terraform {
	required_providers {
		aws = {
			source = "hashicorp/aws"
			version = "~> 5.0"
		}
	}
}

variable "instance_class" {
  description = "The type of the EC2 instance"
  type        = string
  default     = "t2.micro"
}

provider "aws" {}

#On-Demand Instance
resource "aws_instance" "server" {
  ami = "ami-03fa85deedfcac80b"
  instance_type = var.instance_class
  tags = {
    Name = "Telegram-Bot-${formatdate("YYYYMMDD-HHmmss", timestamp())}"
  }
  subnet_id = "subnet-011fcaa2eba4610a3"
  vpc_security_group_ids=["sg-07b0b8944d3dd1bff"]
  associate_public_ip_address = true
  key_name = "febri2023"
}

output "instance_public_ip" {
  value       = aws_instance.server.public_ip
  description = "Public IP of the EC2 instance"
}

output "instance_name" {
  value       = aws_instance.server.tags["Name"]
  description = "Name of the EC2 instance"
}