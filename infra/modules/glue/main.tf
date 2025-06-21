resource "aws_glue_catalog_database" "this" {
    name = var.glue_db_name
    description = var.glue_db_description

}


resource "aws_glue_crawler" "this" {
    database_name = aws_glue_catalog_database.this.name
    name = var.glue_crawler_name
    role = var.glue_iam_role
    table_prefix = var.table_prefix

    s3_target {
        path = var.s3_target_path
      
    }
  
}