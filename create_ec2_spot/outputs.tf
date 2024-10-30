output "instance_public_ip" {
  value       = aws_spot_instance_request.server.public_ip
  description = "Public IP of the EC2 instance"
}

output "instance_name" {
  value = [
    var.instance_count > 0 ? aws_ec2_tag.tag_server[var.instance_count - 1].value : null
  ]
  description = "Name of the first EC2 instance"
}