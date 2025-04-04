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
  role = aws_iam_role.louis-etl-lambda-iam.arn
  package_type = "Image"
  timeout = 300
  environment {
    variables = {
                DB_NAME=var.DB_NAME,
                DB_USERNAME=var.DB_USERNAME,
                DB_HOST=var.DB_HOST,
                DB_PORT=var.DB_PORT,
                DB_PASSWORD=var.DB_PASSWORD
    }
  }
}

data "aws_ecr_image" "louis-api-worker-image" {
  repository_name = "c16-louis-api-worker"
  image_tag = "latest"
}

data "aws_iam_policy_document" "assume_role_worker" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "louis-api-worker-lambda-iam" {
  name               = "c16-louis-api-worker-lambda-iam"
  assume_role_policy = data.aws_iam_policy_document.assume_role_worker.json
}

resource "aws_lambda_function" "api-worker-lambda" {
  function_name = "c16-louis-api-worker-func"
  image_uri = data.aws_ecr_image.louis-api-worker-image.image_uri
  role = aws_iam_role.louis-api-worker-lambda-iam.arn
  package_type = "Image"
}