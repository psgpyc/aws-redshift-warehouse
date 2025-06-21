# AWS Redshift Infrastructure with Glue

This repository provisions a **secure, scalable, production-ready AWS Redshift RA3 cluster** using **Terraform**.   
The setup includes AWS Glue ETL jobs and the Glue Data Catalog to support automated schema discovery, metadata management, and serverless data transformation.  
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
├── boto/                                # Python utilities for AWS SDK (S3, connection, etc.)
│   ├── __init__.py
│   ├── connection.py                    # Boto3 session + client logic
│   ├── s3.py                            # S3 client upload + validation
│   └── tests/                           # Unit tests for boto utilities
│       └── test_s3.py                   # Tests for S3 upload and validation
├── infra/  
│     ├── modules/
│     │   ├── vpc/                  # VPC, subnets, NAT, IGW, route tables
│     │   ├── security/             # Security groups (Redshift, Bastion)
│     │   ├── iam/                  # IAM roles and policies
│     │   ├── redshift/             # Redshift cluster, subnet group
│     │   ├── ec2/                  # Bastion host configuration
│     │   ├── s3/                   # S3 bucket
│     │   ├── glue/                 # Glue bucket
│     ├── environments/
│     │   ├── dev/                  # Dev environment
│     │   │   ├── main.tf
│     │   │   ├── variables.tf
│     │   │   ├── terraform.tfvars (git ignored)
│     │   │   └── backend.tf (git ignored: remote state)
│     │   └── prod/                 # Prod environment (next)
│     ├── policies/
│     │    ├── glue/                                     # Glue policy for ETL
│     │    ├── allow_redshift_s3_bucket_policy.json.tpl  # S3 bucket policy for Redshift log writes
│     │    ├── redshift_access_policy.json               # Access policy for Redshift IAM role
│     │    └── redshift_assume_role_policy.json          # Trust policy for Redshift IAM role
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
