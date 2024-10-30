variable "instance_class" {
  description = "The type of the EC2 instance"
  type        = string
  default     = "t2.micro"
}

variable "instance_count" {
  description = "Count of the EC2 Instances"
  type = number
  default = 0
}