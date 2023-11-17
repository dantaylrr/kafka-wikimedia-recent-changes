from python:3.9.5

# Set docker environment variables
ARG LOCAL_IP

ENV LOCAL_IP ${LOCAL_IP}

WORKDIR /src

# Install poetry
RUN pip install poetry>=1.0.0

# Build files
COPY ./code/producer /src/

# Install project
RUN poetry install --no-dev

# Run source files
CMD ["poetry", "run", "python", "app.py"]