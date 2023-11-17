from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, from_json, current_date
from pyspark.sql.types import StringType

from rcc_utils.schema.schema import generate_schema

# Read the data from the local kafka topic into a spark structured stream - our Kafka topic is of binary types
def _read_data(spark: SparkSession, local_ip: str, topic_name: str):
    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", f"{local_ip}:9092")
        .option("subscribe", f"{topic_name}")
        .option("startingOffsets", "earliest")
        .load()
    )

    return df

# Transform the dataframe into a human-readable dataset, convert our binary columns into strings
def _transform_data(df: DataFrame):
    transformed_df = (
        df.select(col("key").cast(StringType()), col("value").cast(StringType()))
        .withColumn("content", from_json(col("value"), generate_schema()))
        .select("content.*")
        .withColumn("__processing_date", current_date())
    )

    return transformed_df

# Write the data out to the S3 location specified
def _write_data(df: DataFrame, s3_destination: str, s3_checkpoints_destination: str):

    df.writeStream.format("parquet").outputMode("append").partitionBy(
        "__processing_date"
    ).option("path", f"s3a://{s3_destination}").option(
        "checkpointLocation",
        f"s3a://{s3_checkpoints_destination}",
    ).start().awaitTermination()