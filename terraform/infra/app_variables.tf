variable "allowed_cidr" {
  description = "Your public IP in CIDR form (e.g. 203.0.113.7/32). Only this address can reach the load balancer."
  type        = string
}

variable "image_tag" {
  description = "Tag of the image in ECR to run. Tags are immutable, so bump this on every new push."
  type        = string
  default     = "v1"
}

variable "desired_count" {
  description = "Number of running tasks. Use 0 to switch the app off without destroying anything."
  type        = number
  default     = 1
}
