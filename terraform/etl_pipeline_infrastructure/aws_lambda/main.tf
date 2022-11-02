resource "aws_lambda_function" "lambda_function" {
  package_type  = "Image"
  image_uri     = "${var.lambda_image_ecr_uri}:latest"
  function_name = var.function_name
  role          = aws_iam_role.lambda_role.arn
  timeout       = 120
  memory_size   = 1024
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda_function_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_role_role_assume_role_policy.json

  tags = {
    tag-key = "lambda-role"
  }
}

data "aws_iam_policy_document" "lambda_role_role_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "lambda_full_s3_access_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution_role_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name = "/aws/lambda/${aws_lambda_function.lambda_function.function_name}"

  retention_in_days = 30
}
