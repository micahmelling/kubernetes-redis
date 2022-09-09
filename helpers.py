import boto3
import os


def save_file(uid):
    bucket = os.environ['S3_BUCKET']
    # TODO: use a bytestream instead of saving and deleting the file
    with open(f"{uid}.txt", "w") as f:
        f.write(uid)
    s3_client = boto3.client('s3')
    directory = ''
    s3_client.upload_file(f"{uid}.txt", bucket, os.path.join(directory, f"{uid}.txt"))
    os.remove(f"{uid}.txt")
