module "glue_iam_role" {
    source = "../../modules/iam"

    assume_role_policy = file("../../modules/policies/glue/glue_iam_role.json")

    access_policy = ""
}

module "raw_s3_bucket" {
    source = "../../modules/s3"

    bucket_name = var.bucket_name

    bucket_access_policy = templatefile(
        "../../policies/glue/etl_buckts_access_policy.json.tpl",
        {
            bucket_name = var.bucket_name,
            glue_iam_role_arn = module.glue_iam_role.glue_iam_role_arn
        })
}

