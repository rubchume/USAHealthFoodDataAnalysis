variable "aws_region" {
  type = string
  default = "eu-west-3"
}

variable "aws_profile" {
  type = string
  default = "udacity_student"
}

variable "database_name" {
  type = string
  default = "health_data"
}

variable "login" {
  type = string
  default = "dwhuser"
}

variable "password" {
  type = string
  default = "Passw0rd"
}
