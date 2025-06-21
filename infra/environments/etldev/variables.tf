variable "bucket_name" {
    type = string 
}

variable "iam_role_name"{
    type = string
    description = "Name for the IAM role"

}


variable "iam_policy_name" {
    type = string
    description = "Name for the IAM policy"

}


variable "glue_policy_attachments_arns" {
    type = map(string)
    description = "Map of policy attachment names to policy ARNs"

}


# glue

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


