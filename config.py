import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS Configuration
AWS_CONFIG = {
    "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "region_name": os.getenv("AWS_REGION", "eu-west-2"),
}

print(AWS_CONFIG)

# Bedrock Configuration
BEDROCK_CONFIG = {
    "service_name": "bedrock-runtime",
    # 'model_id': 'anthropic.claude-v2',
    # 'model_id': 'anthropic.claude-3-5-sonnet-20240620-v1:0',
    # 'model_id': 'anthropic.claude-3-haiku-20240307-v1:0',
    # 'model_id': 'meta.llama3-8b-instruct-v1:0',
    # "model_id": "amazon.titan-text-lite-v1",
    "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
}

if __name__ == "__main__":
    print(BEDROCK_CONFIG)
    print(AWS_CONFIG)
