import pytest
import boto3
import logging
import pandas as pd
from pathlib import Path
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError
from boto.s3 import validate_client, check_bucket_exists, upload_to_s3, convert_local_excel_to_csv


def test_validate_client_with_valid_s3():
    real_client = boto3.client("s3")
    assert validate_client(real_client) is True

def test_validate_client_wrong_service():
    real_client = boto3.client("glue")
    with pytest.raises(ValueError):
        validate_client(real_client)


def test_validate_client_invalid_type():
    with pytest.raises(TypeError):
        validate_client("not-a-client")


def test_bucket_name_invalid_type():
    mock_client = MagicMock()
    with pytest.raises(TypeError):
        check_bucket_exists(23, mock_client)

def test_check_bucket_exists_success(caplog):
    caplog.set_level(logging.INFO)  

    mock_client = MagicMock()
    mock_client.head_bucket.return_value = None

    check_bucket_exists("simple-bucket", mock_client)

    mock_client.head_bucket.assert_called_once_with(Bucket="simple-bucket")
    assert "Bucket exists and is accessible." in caplog.text

def test_check_bucket_exists_failure(caplog):
    mock_client = MagicMock()
    mock_client.head_bucket.side_effect = ClientError(
        {"Error": {"Code": "404", "Message": "Not Found"}}, "HeadBucket"
    )

    check_bucket_exists("simple-bucket", mock_client)
    assert "Bucket check failed" in caplog.text


def test_upload_to_s3_invalid_path_type():
    mock_client = MagicMock()
    with pytest.raises(TypeError):
        upload_to_s3("not-a-path", bucket="simple-bucket", client=mock_client)


def test_upload_to_s3_bucket_is_none(caplog):
    mock_client = MagicMock()
    path = Path("/tmp/file.csv")
    result = upload_to_s3(path, bucket=None,  client=mock_client)
    assert result is None
    assert "Bucket name is not set" in caplog.text


def test_upload_to_s3_default_object_name():
    mock_client = MagicMock()
    output_filepath = Path("/tmp/file.csv")

    upload_to_s3(output_filepath=output_filepath, bucket="simple-bucket", client=mock_client)

    mock_client.upload_file.assert_called_once_with(output_filepath, "simple-bucket", "raw/file.csv")


def test_upload_to_s3_success():
    mock_client = MagicMock()
    output_filepath = Path("tmp/file.csv")
    result = upload_to_s3(output_filepath=output_filepath, bucket="simple-bucket", client=mock_client)
    mock_client.upload_file.assert_called_once_with(output_filepath, "simple-bucket", "raw/file.csv")


    assert result is True


def test_upload_to_s3_failure(caplog):
    mock_client = MagicMock()
    mock_client.upload_file.side_effect = ClientError(
        {"Error": {"Code": "500", "Message": "Upload Failed"}}, "PutObject"
    )
    output_filepath = Path("tmp/file.csv")

    result = upload_to_s3(output_filepath=output_filepath, bucket="simple-bucket", client=mock_client)

    mock_client.upload_file.assert_called_once_with(output_filepath, "simple-bucket", "raw/file.csv")
    assert result is False
    assert "Error uploading to simple-bucket" in caplog.text
    

@patch("boto.s3.pd.read_excel")
@patch("boto.s3.Path.exists")
def test_convert_local_excel_to_csv_already_exists(mock_path_exists, mock_read_excel):
    mock_path_exists.side_effect = [True, False]

    converted, output_path = convert_local_excel_to_csv()

    assert converted is False
    assert isinstance(output_path, Path)
    mock_read_excel.assert_not_called()

@patch("boto.s3.pd.DataFrame.to_csv")
@patch("boto.s3.pd.read_excel")
@patch("boto.s3.Path.exists", return_value=False)
def test_convert_local_excel_to_csv_not_exists(mock_path_exists, mock_read_excel, mock_to_csv):
    mock_path_exists.side_effect = [False, True]

    dummy_df = pd.DataFrame({
        "col": [1,2,3,4,5]
    })

    mock_read_excel.return_value = dummy_df

    converted, output_path = convert_local_excel_to_csv()

    assert converted is True
    assert isinstance(output_path, Path)

    mock_read_excel.assert_called_once()
    mock_to_csv.assert_called_once_with(output_path, index=False)



    