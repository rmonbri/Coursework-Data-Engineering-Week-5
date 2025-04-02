variable "db_username" {
    type = string
    description = "RDS SQLServer Username"
}

variable "db_password" {
    type = string
    sensitive = true
    description = "RDS SQLServer Password"
}

variable "existing_vpc_name" {
    type = string
    description = "VPC Name"
    default = "c16-VPC"
    
}
variable "existing_db_subnet" {
    type = string
    description = "Subnet Name"
    default = "c16-public-subnet-group"
}