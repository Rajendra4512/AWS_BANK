terraform {
  backend "s3" {
    bucket       = "aws-bank-tfstate-213473482400-ap-southeast-2"
    key          = "aws-bank/development/terraform.tfstate"
    region       = "ap-southeast-2"
    encrypt      = true
    use_lockfile = true
  }
}
