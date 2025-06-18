# AWS Redshift Infrastructure

This repository provisions a **secure, scalable, production-ready AWS Redshift RA3 cluster** using **Terraform**.     
The infrastructure is modular, environment-specific, and aligned with AWS Well-Architected Framework principles.    
This setup is designed for real-world data engineering workloads, enabling data ingestion, transformation, and analytics at scale.  

<img src="https://raw.githubusercontent.com/psgpyc/aws-redshift-warehouse/master/diagrams/aws_redshift_infra.svg" width="100%" />

## Architecture Overview  

The infrastructure includes:

- VPC with public and private subnets across multiple AZs
- IGW and NAT Gateway for internet access
- Bastion EC2 instance in a public subnet for secure Redshift access
- Redshift RA3 cluster deployed across private subnets
- IAM roles for Redshift to access S3 (COPY, UNLOAD, logging)
- S3 bucket for audit logging
- Security groups with least-privilege rules
- Environment separation (dev, prod) via folder structure


## Folder Structure

```bash
aws-redshift-infra/
├── modules/
│   ├── vpc/                  # VPC, subnets, NAT, IGW, route tables
│   ├── security/             # Security groups (Redshift, Bastion)
│   ├── iam/                  # IAM roles and policies
│   ├── redshift/             # Redshift cluster, subnet group
│   ├── ec2/                  # Bastion host configuration
│   └── s3/                   # S3 bucket for Redshift logs
├── environments/
│   ├── dev/                  # Dev environment
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf (optional: remote state)
│   └── prod/                 # Prod environment (next)
├── scripts/
│   └── bastion-setup.sh      # Bastion provisioning script (next: Initially inline with ec2 creation)
├── policies/
│    ├── allow_redshift_s3_bucket_policy.json.tpl  # S3 bucket policy for Redshift log writes
│    ├── redshift_access_policy.json               # Access policy for Redshift IAM role
│    └── redshift_assume_role_policy.json          # Trust policy for Redshift IAM role
├── diagrams/
│   └── redshift-architecture.svg
├── .gitignore
├── README.md
└── Makefile (next)

```

## Security Best Practices

- No public access to Redshift nodes  
- SSH access restricted to Bastion only  
- IAM roles follow **least privilege**  
- Sensitive outputs excluded from state (e.g., passwords via Secrets Manager or environment variables)  
- Terraform `.tfvars` excluded from version control  

## Prerequisites

- [Terraform CLI](https://developer.hashicorp.com/terraform/downloads)  
- AWS CLI configured with appropriate access  
- SSH key pair for EC2 access  
- IAM User Permissions to provision VPC, Redshift, IAM, EC2, S3, etc

## License

MIT License – feel free to use, modify, and contribute.
