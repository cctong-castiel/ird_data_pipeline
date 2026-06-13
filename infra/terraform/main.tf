provider "aws" {
  region = "ap-northeast-1"
}

# New IAM User for OpenSearch management
resource "aws_iam_user" "opensearch_admin" {
  name = "OpenSearch-Admin-User"
}

resource "aws_iam_user_policy_attachment" "attach_full_access" {
  user       = aws_iam_user.opensearch_admin.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonOpenSearchServiceFullAccess"
}

# Access Key for this user (to be used in your environment)
resource "aws_iam_access_key" "opensearch_admin_key" {
  user = aws_iam_user.opensearch_admin.name
}

output "opensearch_admin_access_key_id" {
  value = aws_iam_access_key.opensearch_admin_key.id
}

output "opensearch_admin_secret_access_key" {
  value     = aws_iam_access_key.opensearch_admin_key.secret
  sensitive = true
}

# IAM
# 1. Define your existing IAM Usernames here
// ...existing code...
locals {
    existing_usernames = [
        "OpenSearch-RAG-User"
    ]
}
# 2. Dynamically fetch details for all listed IAM Users
data "aws_iam_user" "existing_users" {
  for_each  = toset(local.existing_usernames) # Changed from locals.existing_usernames
  user_name = each.value
}

# 3. Define the OpenSearch Domain
# OpenSearch Domain
resource "aws_opensearch_domain" "ird_opensearch" {
  domain_name    = "ird-data-pipeline-domain"
  engine_version = "OpenSearch_2.11"

  cluster_config {
    instance_type = "t3.small.search"
    # For a production environment, you would increase the number of nodes
    # and use a larger instance type.
    dedicated_master_enabled = false
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 20
  }

  # Access policy to allow access to the domain
  # In a real scenario, you should restrict this to specific IAM roles/users
  access_policies = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = [for u in data.aws_iam_user.existing_users : u.arn]
        }
        Action   = "es:*"
        Resource = "arn:aws:es:ap-northeast-1:*:domain/ird-data-pipeline-domain/*"
      }
    ]
  })

  # Enable fine-grained access control for better security
  # plugin_artifacts is not a valid block for aws_opensearch_domain in this context.
  # If specific plugins are needed, they are typically handled via the AWS Console or API.

  # Ensure the domain is created with the necessary settings for k-NN
  # Note: k-NN is enabled by default in newer OpenSearch versions, 
  # but specific index settings are handled via the API/Client.
}

# S3 Bucket for data storage (using same naming pattern and region)
resource "aws_s3_bucket" "data_storage" {
  bucket = "ird-data-pipeline-storage"
}

# Output the endpoint for use in the application's .env file
output "opensearch_endpoint" {
  value       = aws_opensearch_domain.ird_opensearch.endpoint
  description = "The endpoint for the OpenSearch domain"
}

output "domain_arn" {
  value       = aws_opensearch_domain.ird_opensearch.arn
  description = "The ARN of the OpenSearch domain"
}
