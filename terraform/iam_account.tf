resource "aws_iam_user" "user_access_bucket" {
  name = "access-github-bucket"
}

resource "aws_iam_policy" "policy_access_bucket" {
  name = "access-github-bucket"
  description = "Policy allowing to access the S3 bucket with name l30bola-github-profile."

  policy = <<-POLICY
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "s3:DeleteObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutObject"
        ],
        "Effect": "Allow",
        "Resource": [
          "arn:aws:s3:::l30bola-github-profile",
          "arn:aws:s3:::l30bola-github-profile/*"
        ]
      }
    ]
  }
  POLICY
}

resource "aws_iam_group" "group_access_bucket" {
  name = "access-github-bucket"
}

resource "aws_iam_group_policy_attachment" "attach_group_access_bucket" {
  group = aws_iam_group.group_access_bucket.name
  policy_arn = aws_iam_policy.policy_access_bucket.arn
}

resource "aws_iam_user_group_membership" "attach_user_access_bucket" {
  user = aws_iam_user.user_access_bucket.name
  groups = [
    aws_iam_group.group_access_bucket.name,
  ]
}