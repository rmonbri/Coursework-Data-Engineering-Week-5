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

data "aws_ecr_image" "louis-etl-image" {
  repository_name = "c16-louis-measurements-etl"
  image_tag = "latest"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "louis-etl-lambda-iam" {
  name               = "c16-louis-measurements-lambda-iam"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_lambda_function" "etl-measurements-lambda" {
  function_name = "c16-louis-measurements-etl"
  image_uri = data.aws_ecr_image.louis-etl-image.image_uri
  role = aws_iam_role.louis-etl-lambda-iam
  package_type = "Image"
  environment {
    variables = {
                DB_NAME=var.DB_NAME,
                DB_USERNAME=var.DB_USERNAME,
                DB_HOST=var.DB_HOST,
                DB_PORT=var.DB_PORT,
                DB_PASSWORD=var.DB_PASSWORD,
    }
  }
}