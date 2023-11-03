import logging
from sys import stdout
import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, current_date

from pyspark.sql.types import StructType, StructField, StringType, BooleanType, LongType

logging.basicConfig(level=logging.INFO, stream=stdout)
logger = logging.getLogger(name=__name__)


def generate_schema():
    return StructType(
        [
            StructField("$schema", StringType(), True),
            StructField(
                "meta",
                StructType(
                    [
                        StructField("domain", StringType(), True),
                        StructField("dt", StringType(), True),
                        StructField("id", StringType(), True),
                        StructField("offset", LongType(), True),
                        StructField("partition", LongType(), True),
                        StructField("request_id", StringType(), True),
                        StructField("stream", StringType(), True),
                        StructField("topic", StringType(), True),
                        StructField("uri", StringType(), True),
                    ]
                ),
                True,
            ),
            StructField("bot", BooleanType(), True),
            StructField("comment", StringType(), True),
            StructField("id", LongType(), True),
            StructField("namespace", LongType(), True),
            StructField("notify_url", StringType(), True),
            StructField("parsedcomment", StringType(), True),
            StructField("server_name", StringType(), True),
            StructField("server_script_path", StringType(), True),
            StructField("server_url", StringType(), True),
            StructField("timestamp", LongType(), True),
            StructField("title", StringType(), True),
            StructField("title_url", StringType(), True),
            StructField("type", StringType(), True),
            StructField("user", StringType(), True),
            StructField("wiki", StringType(), True),
        ]
    )


def read_and_write_stream(spark: SparkSession, s3_bucket: str):
    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "wikimedia-changes")
        .option("startingOffsets", "earliest")
        .load()
    )

    df1 = (
        df.select(col("key").cast(StringType()), col("value").cast(StringType()))
        .withColumn("content", from_json(col("value"), generate_schema()))
        .select("content.*")
        .withColumn("__processing_date", current_date())
    )

    df1.writeStream.format("parquet").outputMode("append").partitionBy(
        "__processing_date"
    ).option("path", f"s3a://{s3_bucket}/wikimedia-changes").option(
        "checkpointLocation",
        f"s3a://{s3_bucket}/wikimedia-changes-checkpoints",
    ).start().awaitTermination()


if __name__ == "__main__":
    # Get access keys for authorisation - in the real world this would be handled by IAM / instance profiles
    try:
        AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
        AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
        S3_BUCKET = os.environ["AWS_S3_RAW_STORAGE_BUCKET"]
    except KeyError as ex:
        raise Exception(
            f"{ex} - AWS Access Keys not set correctly, try re-setting & trying again."
        )

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

    # Read & write from our source stream
    read_and_write_stream(spark=spark)
