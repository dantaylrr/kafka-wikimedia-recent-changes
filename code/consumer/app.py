import logging
from sys import stdout
import os

from pyspark.sql import SparkSession

from rcc_utils.transformations.transform import _read_data, _transform_data, _write_data

logging.basicConfig(level=logging.INFO, stream=stdout)
logger = logging.getLogger(name=__name__)

# Get access keys for authorisation - in the real world this would be handled by IAM / instance profiles
try:
    LOCAL_IP = os.environ["LOCAL_IP"]
    AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    S3_BUCKET = os.environ["AWS_S3_RAW_STORAGE_BUCKET"]
    S3_CHECKPOINTS_BUCKET = os.environ["AWS_S3_CHECKPOINTS_STORAGE_BUCKET"]
except KeyError as ex:
    raise Exception(
        f"{ex} - AWS Access Keys not set correctly, try re-setting & trying again."
    )


# Orchestrator
def main():
    # Init spark
    spark = (
        SparkSession.builder.master("local[*]")
        .appName("streaming_from_kafka")
        .config("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        )
        .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_ACCESS_KEY)
        .getOrCreate()
    )

    df = _read_data(spark=spark, local_ip=LOCAL_IP, topic_name="wikimedia-changes")

    transformed_df = _transform_data(df=df)

    _write_data(
        df=transformed_df,
        s3_destination=f"{S3_BUCKET}/wikimedia-changes",
        s3_checkpoints_destination=f"{S3_CHECKPOINTS_BUCKET}/wikimedia-changes",
    )


if __name__ == "__main__":
    main()
