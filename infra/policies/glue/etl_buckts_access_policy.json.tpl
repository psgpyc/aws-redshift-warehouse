{
    "Version":  "2012-10-17",
    "Statement":  [{
        "Effect": "Allow",
        "Principal": {
            "AWS":  "${glue_iam_role_arn}"
        },
        "Action":  [
            "s3:GetObject",
            "s3:PutObject"
        ],

        "Resource":  [
            "s3://${bucket_name}",
            "s3://${bucket_name}/*"
        ]
    }]
}

