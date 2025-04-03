terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.92.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

resource "aws_s3_bucket" "c16-louis-bucket" {
    bucket = "c16-louis-data"
}