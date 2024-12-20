output "instance_public_ips" {
  value = { for name, instance in aws_spot_instance_request.server : name => instance.public_ip }
  description = "Public IPs of the EC2 spot instances"
}