"""Module for handling S3 operations including client validation, bucket checks,
conversion of local Excel files to CSV, and uploading files to S3."""

import os
import boto3
import botocore
import logging
import botocore.client
import pandas as pd
from pathlib import Path
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from connection import get_session_obj

def validate_client(s3c: botocore.client.BaseClient) -> bool:
    """Validate that the provided client is a boto3 S3 client.

    Args:
        s3c (botocore.client.BaseClient): The boto3 client to validate.

    Raises:
        TypeError: If the client is not a boto3 client.
        ValueError: If the client is not an S3 client.

    Returns:
        bool: True if the client is a valid S3 client.
    """
    if not isinstance(s3c, botocore.client.BaseClient):
        raise TypeError("Expected a boto3 client, but got something else...")
    
    if s3c.meta.service_model.service_name != "s3":
        raise ValueError("Client is not an S3 client.")
    
    return True
    

def check_bucket_exists(bucket_name: str, client: botocore.client.BaseClient) -> None:
    """Check if the specified S3 bucket exists and is accessible.

    Args:
        bucket_name (str): The name of the S3 bucket.
        client (botocore.client.BaseClient): The S3 client to use.

    Raises:
        TypeError: If the bucket_name is not a string.
    """
    if not isinstance(bucket_name, str):
        raise TypeError(f"Expected string for bucket_name, but got {type(bucket_name).__name__}")
    
    try: 
        client.head_bucket(Bucket=bucket_name)
        logging.info("Bucket exists and is accessible.")
    except ClientError as e:
        logging.error(f"Bucket check failed: {e}")


def convert_local_excel_to_csv(input_filename: str = "Online Retail.xlsx", output_filename: str = "retail.csv") -> tuple:
    """Convert a local Excel file to CSV format if the CSV does not already exist.

    Args:
        input_filename (str, optional): The Excel file to convert. Defaults to "Online Retail.xlsx".
        output_filename (str, optional): The output CSV filename. Defaults to "retail.csv".

    Returns:
        tuple: (bool indicating if conversion was done, Path to the output CSV or None)
    """
        
    data_dir = Path(__file__).parent.parent / "data"
    input_path = data_dir / input_filename
    output_path = data_dir / output_filename
    if output_path.exists():
        return (False, output_path)

    if input_path.exists():
        df = pd.read_excel(input_path)
        df.to_csv(output_path, index=False)
        logging.info(f"Converted '{input_filename}' to '{output_filename}'")
        return (True, output_path)
    else:
        logging.warning(f"Input file '{input_filename}' not found in {data_dir}")
        return (False, None)


def upload_to_s3(output_filepath: Path, bucket: str, object_name:str = None, client = botocore.client.BaseClient) -> bool:
    """Upload a file to an S3 bucket.

    Args:
        output_filepath (Path): The local file path to upload.
        bucket (str): The target S3 bucket name.
        object_name (str, optional): The S3 object name. If None, defaults to 'raw/{filename}'.
        client (botocore.client.BaseClient): The S3 client to use.

    Raises:
        TypeError: If output_filepath is not a Path object.

    Returns:
        bool: True if upload succeeded, False otherwise.
    """

    if not isinstance(output_filepath, Path):
        raise TypeError(f"Expected Path for file path, but got {type(output_filepath).__name__}")
    
    if object_name is None:
        object_name = f"raw/{output_filepath.name}"
    
    if bucket is None:
        logging.error("Bucket name is not set.")
        return
    
    try:
        logging.info("Starting the upload......")
        client.upload_file(output_filepath, bucket, object_name)
    except ClientError as e:
        logging.error(f"Error uploading to {bucket}: {e}")
        return False
    return True

     
def main(client):
    """Main function to validate client, check bucket, convert Excel to CSV, and upload to S3.

    Args:
        client (botocore.client.BaseClient): The S3 client to use.
    """
    bucket = os.environ.get("BUCKET_NAME")  
    if not bucket:
        logging.error("Environment variable BUCKET_NAME is not set.")
        return

    if not validate_client(s3c=client): 
        logging.error("Invalid S3 client.")
        return
    
    check_bucket_exists(bucket, client=client)

    is_converted, output_filepath = convert_local_excel_to_csv()
    if not is_converted:
        logging.warning("Data conversion skipped.")


    upload_status = upload_to_s3(output_filepath=output_filepath, bucket=bucket, client=client)
    if upload_status:
        logging.info(f"Successfully uploaded to {bucket}..")
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    s3c = get_session_obj(service="s3")
    main(client=s3c)
