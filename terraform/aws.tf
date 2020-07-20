provider "aws" {
  region = "us-east-1"
}

terraform {
 backend "s3" {
    bucket = "l30bola-github-profile"
    key    = "terraform/state.tfstate"
    region = "us-east-1"
  }
}