output "ecr_scraper_repository_url" {
    value=module.ecr_lambda_repositories.ecr_repository_variables["lambda_image"]
}
