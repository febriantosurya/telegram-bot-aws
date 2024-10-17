terraform {
	required_providers {
		aws = {
			source = "hashicorp/aws"
			version = "~> 5.0"
		}
	}
}

provider "aws" {
	region = "ap-southeast-1"
}

data "aws_instances" "all" {}

output "instance_ids" {
  value = [for instance in data.aws_instances.all.ids : instance]
}