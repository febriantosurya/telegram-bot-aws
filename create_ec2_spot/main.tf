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
  type = string
  default = "t2.micro"
}

provider "aws" {}

resource "aws_launch_template" "server_template" {
  name_prefix   = "telegram-bot"
  image_id      = "ami-03fa85deedfcac80b"
  instance_type = var.instance_class
  key_name      = "febri2023"

  network_interfaces {
    associate_public_ip_address = true
    subnet_id                   = "subnet-011fcaa2eba4610a3"
    security_groups             = ["sg-07b0b8944d3dd1bff"]
  }

  tag_specifications {
    resource_type = "instance"

    tags = {
      Name = "Telegram-Bot-${formatdate("YYYYMMDD-HHmmss", timestamp())}"
    }
  }
}

resource "aws_spot_instance_request" "server" {
  launch_template {
    id      = aws_launch_template.server_template.id
    version = "$Latest"
  }

  spot_type = "persistent"
}

#data "aws_instance" "spot_instance" {
#  instance_id = aws_spot_instance_request.server.spot_instance_id
#}
#
#output "instance_public_ip" {
#  value       = data.aws_instance.spot_instance.public_ip
#  description = "Public IP of the EC2 instance"
#}

#output "instance_name" {
#  value       = data.aws_instance.spot_instance.tags["Name"]
#  description = "Name of the EC2 instance"
#}