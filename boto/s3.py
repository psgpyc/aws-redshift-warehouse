import os
import boto3
import botocore
import logging
import pandas as pd
from pathlib import Path
from botocore.exceptions import ClientError
from connection import get_session_obj

def validate_client(s3c: botocore.client.BaseClient) -> bool:
    if not isinstance(s3c, botocore.client.BaseClient):
        raise TypeError("Expected a boto3 client, but got something else...")
    
    if s3c.meta.service_model.service_name != "s3":
        raise ValueError("Client is not an S3 client.")
    
    return True
    

def check_bucket_exists(bucket_name: str, client: botocore.client.BaseClient) -> None:
    if not isinstance(bucket_name, str):
        raise TypeError(f"Expected string for bucket_name, but got {type(bucket_name).__name__}")
    
    try: 
        client.head_bucket(Bucket=bucket_name)
        logging.info("Bucket exists and is accessible.")
    except ClientError as e:
        logging.error(f"Bucket check failed: {e}")


def convert_local_excel_to_csv(input_filename: str = "Online Retail.xlsx", output_filename: str = "retail.csv") -> bool:
        
        data_dir = Path(__file__).parent.parent / "data"
        input_path = data_dir / input_filename
        output_path = data_dir / output_filename
        if output_path.exists():
            return False

        if input_path.exists():
            df = pd.read_excel(input_path)
            df.to_csv(output_path, index=False)
            logging.info(f"Converted '{input_filename}' to '{output_filename}'")
            return True
        else:
            logging.warning(f"Input file '{input_filename}' not found in {data_dir}")
            return False


def upload_to_s3():
    pass

 
def main(client):
    bucket = os.environ.get("BUCKET_NAME")  
    if not bucket:
        logging.error("Environment variable BUCKET_NAME is not set.")
        return

    if not validate_client(s3c=client): 
        logging.error("Invalid S3 client.")
        return
    
    check_bucket_exists(bucket, client=client)

    if not convert_local_excel_to_csv():
        logging.warning("Data conversion skipped.")
    



       

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    s3c = get_session_obj(service="s3")
    main(client=s3c)
