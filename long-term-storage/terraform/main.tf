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

data "aws_ecr_image" "louis-storage-image" {
  repository_name = "c16-louis-storage-lambda"
  image_tag = "latest"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = [
      "sts:AssumeRole"
      ]
      
  }
}

resource "aws_iam_role" "louis-storage-lambda-iam" {
  name               = "c16-louis-storage-lambda-iam"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_lambda_function" "long-term-storage-lambda" {
  function_name = "c16-louis-storage"
  image_uri = data.aws_ecr_image.louis-storage-image.image_uri
  role = aws_iam_role.louis-storage-lambda-iam.arn
  package_type = "Image"
  environment {
    variables = {
                DB_NAME=var.DB_NAME,
                DB_USERNAME=var.DB_USERNAME,
                DB_HOST=var.DB_HOST,
                DB_PORT=var.DB_PORT,
                DB_PASSWORD=var.DB_PASSWORD,
                PRODUCTION_MODE=var.PRODUCTION_MODE,
                BUCKET_NAME=var.BUCKET_NAME

    }
  }
}