variable "DB_USERNAME" {
  type = string
  description = "SQL Server Database username"
}

variable "DB_PASSWORD" {
  type = string
  description = "SQL Server Database password"
  sensitive = true
}

variable "DB_HOST" {
  type = string
  description = "SQL Server Database host"
}

variable "DB_NAME" {
  type = string
  description = "SQL Server Database name"
}

variable "DB_PORT" {
  type = string
  description = "SQL Server Database port"
}

variable "AWS_ACCESS_KEY_ID" {
  type = string
  description = "AWS Key"
}

variable "AWS_SECRET_ACCESS_KEY" {
  type = string
  description = "AWS Secret"
}

variable "existing_vpc_name" {
  type = string
  description = "VPC Name"
}