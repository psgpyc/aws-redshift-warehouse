import boto3

session = boto3.Session(profile_name="sikka")

glue = session.client("glue")

def create_glue_db():
    db = glue.create_database(
        DatabaseInput={
            "Name":  "tengus",
            "Description": "A logical name space",
        }
    )
    return db


print(create_glue_db())
