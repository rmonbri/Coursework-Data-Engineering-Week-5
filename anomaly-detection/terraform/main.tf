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


data "aws_ecr_image" "louis-alert-image" {
  repository_name = "c16-louis-anomaly-alert-ecr"
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

data "aws_iam_policy_document" "ses_permissions" {
  statement {
    effect    = "Allow"
    actions   = ["ses:SendEmail", "ses:SendRawEmail"]
    resources = ["arn:aws:ses:eu-west-2:129033205317:identity/*" ]
  }
}




resource "aws_iam_role" "louis-anomaly-alert-lambda-iam" {
  name               = "c16-louis-anomaly-alert-lambda-iam"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "ses_policy" {
  name   = "c16-louis-anomaly-alert-ses-policy"
  policy = data.aws_iam_policy_document.ses_permissions.json
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/c16-louis-anomaly-alert"
  retention_in_days = 14
}

resource "aws_lambda_function" "anomaly-alert-lambda" {
  function_name = "c16-louis-anomaly-alert"
  image_uri = data.aws_ecr_image.louis-alert-image.image_uri
  role = aws_iam_role.louis-anomaly-alert-lambda-iam.arn
  package_type = "Image"
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
