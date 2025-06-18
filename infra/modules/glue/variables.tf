variable "glue_db_name" {
    type = string  
}

variable "glue_db_description" {
    type = string
    default = "A logical namespace for glue catalog database"
  
}

variable "glue_crawler_name" {
    type = string
  
}

variable "glue_iam_role" {
    type = string
  
}


variable "s3_target_path" {
    type = string
  
}

variable "table_prefix" {
    type = string
    description = "Optional Table Prefix"
    default = ""
  
}