# **Data Ingestion of Wikipedia recent changes.**

# **Table of Contents.**

<ol>
<li><a href="#todo">TODO</a></li>
<li><a href="#project-outline">Project outline</a></li>
<li><a href="#worflow">Workflow</a></li>
<li><a href="#event-schemas">Event schemas</a></li>
<li><a href="#prerequisites">Prerequisites</a></li>
<li><a href="#setup">Setup</a></li>
<li><a href="#local-development">Local development</a></li>
<li><a href="#running-apps">Running apps</a></li>
<li><a href="#appendix---directory-structure">Appendix - Directory structure</a></li>
</ol>

# **TODO.**

1). Appropriate tests for both producer & consumer applications. \
2). Tidying up & improvements of source code (i.e. producer currently has some logging bugs, consumer Spark code is fairly basic / vanilla). \
3). Terraform code for AWS infrastructure. \
4). Use of parameter store (or equivalent) for secret management. \
5). Kafka schema registry for producer & consumer schema contracts \
6). `make help` & general makefile improvements.
7). Containerisation of Kafka & Spark. \
8). Nicer way to manage virtual-env's in mono-repo (?). \
9). Migrate to cloud (unsure because of cost) (?).

# **Project outline.**

The aim of this project is to produce two standalone applications, a producer & a consumer, centred around a local kafka topic acting as our message bus.

Wikimedia make available a set of free-to-use streams, centred around their Wikipedia websites. For this specific data pipeline, we will be leveraging their [**recent changes**](https://www.mediawiki.org/wiki/API:Recent_changes_stream) stream. This stream outputs any & all changes made to any wikipedia page, each represented as a single data point (think of this as event data).

# **Workflow.**

High-level architecture diagram:

<img src='./media/ArchitectureHL.png'>

<br>

The workflow aims to do the following, in order:

* The producer application will listen to the recent changes wikimedia stream endpoint whilst running.
* The producer will leverage the `confluent_kafka` python library to post each event to a local kafka topic (in this case called "**wikimedia-changes**".)
* The kafka consumer application (a spark structured streaming applications) will consume from the same kafka topic in parallel.
* The spark streaming application will then save each batch of messages in S3 as parquet.

# **Event schema.**

Full details of the recent changes event schema can be found [here](https://github.com/wikimedia/mediawiki-event-schemas/blob/master/jsonschema/mediawiki/recentchange/current.yaml).

# **Prerequisites.**

* Python ^=3.9.
* [Poetry](https://python-poetry.org/docs/) for builds.
* An AWS account for cloud infrastructure.
* Docker installed on your system (`brew install docker` on mac).
* Kafka installed & setup on your system (`brew install kafka` on mac) - for an in-depth guide into running kafka locally on mac (both for x86 & arm architectures), follow the guide [here](https://github.com/dantaylrr/kafka-beginners/blob/main/notes/Part%203%20-%20Running%20Kafka%20Locally/Introduction.md).

# **Setup.**

In an enterprise scenario, Kafka would be hosted in-cloud (maybe using MSK, Conduktor, etc.), our producer application run on EC2 or ECS & our consumer application run on something like Glue, EMR or Databricks.

As we are running kafka & applications locally & not in-cloud, there requires a little bit of manual set-up in order to get things to work (as things stand).

### **Cloud (AWS) infrastructure setup.**

_**TODO - Terraform code for cloud infrastructure provisioning.**_

In order for our consumer to stream events directly into our S3 bucket, we need to create a few cloud resources:

* An S3 bucket for our data (call this whatever you want).
* An S3 bucket for Spark checkpoints (call this whatever you want).
* An IAM user for our Kafka consumer to assume, with the correct permissions to put records in both of our new S3 buckets.
* Programmatic access keys for new IAM user (these will be dynamically passed to our consumer via. environment variables).

### **Exposing our Kafka broker.**

In order for our dockerised application to communicate with our local kafka infrastructure, we need to expose the the broker to our local network.

### **Steps.**

1). Find your local IP address (this can be done using `ipconfig getifaddr en0` in your terminal).

2). Open the following kafka file in any text editor: `/opt/homebrew/etc/kafka/kraft/server.properties` (if on M1 mac).

3). Find the property `advertised.listeners` & modify the value so that the property resembles the following:

`advertised.listeners=PLAINTEXT://<local_ip>:9092`

**Make sure to save your changes.**

4). Open up a new terminal window & run the following command to start a local kafka server:

`kafka-server-start /opt/homebrew/etc/kafka/kraft/server.properties`

### Make sure Docker is running.

Make sure Docker Daemon is running locally, you can verify that Docker is running by running something like:

`docker container ls`

from the terminal.

### **.env file.**

We will be utilising environment variables as the main source of our secrets for each application.

Create a local `.env` file in the root of this directory with the following key-value pairs:

```
LOCAL_IP=<local_ip_value>
AWS_ACCESS_KEY=<aws_access_key_value>
AWS_SECRET_ACCESS_KEY=<aws_secret_key_value>
AWS_S3_RAW_STORAGE_BUCKET=<s3_bucket_name_for_data>
AWS_S3_CHECKPOINTS_STORAGE_BUCKET=<s3_bucket_name_for_checkpoints>
```

Once done, you can export all of the variables inside this file as environment variables by opening a terminal at the root of this repository & running:

```
export $(xargs < .env)
```

& can be verified by either `printenv` or `echo $LOCAL_IP`.

**Make sure NOT to commit any secrets to remote, .gitignore should ignore this file completely but make sure to be careful.**

# **Local development.**

Start by cloning to repo locally:

```
git clone git@github.com:dantaylrr/kafka-wikimedia-recent-changes.git
```

& navigating to the root of this repository:

```
cd kafka-wikimedia-recent-changes
```

Running `make setup` will create 3 different virtual-environments:

1). A virtual-env. located at the root of this directory - use this for non-python related development (i.e. Makefile changes). \
2). A virtual-env. for the producer application, under the `code/producer` directory - use this for local producer development. \
3). A virtual-env. for the consumer application, under the `code/consumer` directory - use this for local consumer development.

For application development of either the producer or consumer, navigate to the root of the applications' directory & run `source .venv/bin/activate`.

# **Running apps.**

We can run both our producer & consumer apps using the following `make` commands:

* Producer - `make run-producer`
* Consumer - `make run-consumer`

# **Appendix - Directory structure.**

```
📦 kafka-wikimedia-producer
.github/
└── workflows/
    └── black.yaml
code/
├── consumer/
│   ├── rcc_utils/
│   │   ├── schema/
│   │   │   ├── .
│   │   │   ├── .
│   │   │   └── .
│   │   └── transformations/
│   │       ├── .
│   │       ├── .
│   │       └── .
│   ├── app.py
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── README.md
└── producer/
    ├── rcp_utils/
    │   ├── api/
    │   │   ├── .
    │   │   ├── .
    │   │   └── .
    │   └── kafka/
    │       ├── .
    │       ├── .
    │       └── .
    ├── app.py
    ├── poetry.lock
    ├── pyproject.toml
    └── README.md
docker/
└── producer.Dockerfile
media/
└── ArchitectureHL.png
tests/
└── (placeholder)
.dockerignore
.flake8
.gitignore
.pre-commit-config.yaml
.secrets.bassline
docker-compose.yaml
Makefile
README.md
```
