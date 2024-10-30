terraform {
	required_providers {
		aws = {
			source = "hashicorp/aws"
			version = "~> 5.0"
		}
	}
}

provider "aws" {}

resource "aws_spot_instance_request" "server" {
  ami = "ami-03fa85deedfcac80b"
  instance_type = var.instance_class
  tags = {
    Name = "Telegram-Bot-${formatdate("YYYYMMDD-HHmmss", timestamp())}"
  }
	spot_type = "persistent"
  subnet_id = "subnet-011fcaa2eba4610a3"
  vpc_security_group_ids=["sg-07b0b8944d3dd1bff"]
  key_name = "febri2023"
	associate_public_ip_address = true
	wait_for_fulfillment = true
}