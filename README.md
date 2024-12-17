# Field Mapping Service

A FastAPI application that uses AWS Bedrock to generate field mappings based on input data fields.

## Prerequisites

- Python 3.11+
- AWS credentials configured with access to Bedrock
- Docker (for containerization)

## Local Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials:
- Ensure your AWS credentials are configured in `~/.aws/credentials` or set the appropriate environment variables.
- Set the AWS region:
```bash
export AWS_REGION=us-east-1
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Running Tests

```bash
pytest tests/
```

## API Usage

Send a POST request to `/generate-mapping` with the following JSON structure:

```json
{
  "Account_name": "example_account",
  "Root_directory": "example_directory",
  "Excel_data_fields": ["field1", "field2"]
}
```

The response will be:

```json
{
  "Account_name": "example_account",
  "Root_directory": "example_directory",
  "field_mappings": {
    "field1": "mapped_field1",
    "field2": "mapped_field2"
  }
}
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t field-mapping-service .
```

2. Run the container:
```bash
docker run -p 8000:8000 field-mapping-service
```

## AWS Lambda Deployment

1. Build the Docker image for Lambda:
```bash
docker build -t field-mapping-lambda .
```

2. Tag and push the image to Amazon ECR:
```bash
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com
docker tag field-mapping-lambda:latest YOUR_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com/field-mapping-lambda:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.eu-west-2.amazonaws.com/field-mapping-lambda:latest
```

3. Create a Lambda function using the container image and configure the function URL for HTTP access. 