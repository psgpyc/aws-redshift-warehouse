module "glue_iam_role" {
    source = "../../modules/iam"

    iam_role_name = var.iam_role_name

    iam_policy_name = var.iam_policy_name

    assume_role_policy = file("../../policies/glue/glue_iam_role.json")

    access_policy = templatefile(
        "../../policies/glue/glue_access_policy.json.tpl",
        {
            bucket_name = var.bucket_name
        }
    
    )
}

resource "aws_iam_role_policy_attachment" "glue_aws_managed_policies" {
    for_each = var.glue_policy_attachments_arns

    role = module.glue_iam_role.i_am_role_name
    policy_arn = each.value
    
}


module "raw_s3_bucket" {
    source = "../../modules/s3"

    bucket_name = var.bucket_name

    bucket_access_policy = templatefile(
        "../../policies/glue/etl_buckts_access_policy.json.tpl",
        {
            bucket_name = var.bucket_name,
            glue_iam_role_arn = module.glue_iam_role.iam_role_arn
        })
}


module "glue" {
    source = "../../modules/glue"

    glue_db_name = var.glue_db_name

    glue_db_description = var.glue_db_description

    glue_crawler_name = var.glue_crawler_name

    glue_iam_role = module.glue_iam_role.iam_role_arn

    s3_target_path = "s3://${module.raw_s3_bucket.bucket_name}"

  
}

