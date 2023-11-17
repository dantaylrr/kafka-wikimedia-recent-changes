import logging
from sys import stdout

from pyspark.sql.types import StructType, StructField, StringType, BooleanType, LongType

logging.basicConfig(level=logging.INFO, stream=stdout)
logger = logging.getLogger(name=__name__)

# Hello!


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
