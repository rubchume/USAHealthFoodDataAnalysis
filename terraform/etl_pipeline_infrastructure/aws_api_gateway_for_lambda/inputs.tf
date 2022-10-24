variable "aws_lambda_function" {
  type = object({
    invoke_arn = string
    function_name = string
  })
}
