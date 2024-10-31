output "instance_public_ips" {
  value = format("List of IPs:\n%s", join("\n", [
    for name, instance in aws_spot_instance_request.server : format("- %s (%s)", name, tostring(instance.public_ip))
  ]))
  description = "Public IPs of the EC2 spot instances"
}