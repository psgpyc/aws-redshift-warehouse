variable "iam_role_name"{
    type = string
    description = "Name for the IAM role"

}


variable "iam_policy_name" {
    type = string
    description = "Name for the IAM policy"

}

variable "assume_role_policy" {
    type = string
    description = "Assume Role policy for the IAM role"
  
}

variable "access_policy" {
    type = string
    description = "Access policy for the IAM role"
  
}