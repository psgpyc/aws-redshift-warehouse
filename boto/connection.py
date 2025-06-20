import os
import botocore
import boto3
import botocore.client
from dotenv import load_dotenv

load_dotenv()

def get_session_obj(service: str) -> botocore.client.BaseClient:
    session = boto3.Session(profile_name=os.environ.get("PROFILE_NAME"))
    return session.client(service)

