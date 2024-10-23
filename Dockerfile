FROM python:3.9

WORKDIR /auth-service

# Copy the rest of the application code
COPY . /auth-service

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /auth-service/requirements.txt

