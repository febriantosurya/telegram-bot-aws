locals {
  lines = split("\n", trim(file("spot_name.txt"), " \t\n"))
  spots = [
    for line in local.lines : {
      name = split(",", line)[0]
      type = split(",", line)[1]
    } if length(line) > 0
  ]
}

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
  for_each = { for spot in local.spots : spot.name => spot }
  ami = "ami-03fa85deedfcac80b"
  instance_type = each.value.type
	spot_type = "persistent"
  subnet_id = "subnet-011fcaa2eba4610a3"
  vpc_security_group_ids=["sg-07b0b8944d3dd1bff"]
  key_name = "febri2023"
	associate_public_ip_address = true
  tags = { Name = each.value.name }
	wait_for_fulfillment = true
}

output "instance_public_ips" {
  value = { for name, instance in aws_spot_instance_request.server : name => instance.public_ip }
  description = "Public IPs of the EC2 spot instances"
}