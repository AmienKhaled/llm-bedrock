from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from mangum import Mangum
from langchain_aws import BedrockLLM
from langchain.prompts import PromptTemplate
import os
import json
from dotenv import load_dotenv
import uvicorn

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Field Mapping Service")
handler = Mangum(app)

# Initialize Bedrock client
bedrock = BedrockLLM(
    credentials_profile_name="default",
    model_id=os.getenv("MODEL_ID", "amazon.titan-text-lite-v1"),
    region_name=os.getenv("AWS_REGION", "eu-west-2"),
    temperature=0
)

class FieldMappingRequest(BaseModel):
    Account_name: str
    Root_directory: str
    Excel_data_fields: List[str]

class FieldMapping(BaseModel):
    Account_name: str
    Root_directory: str
    field_mappings: dict

MAPPING_PROMPT = PromptTemplate(
    input_variables=["fields"],
    template="""
Given the following information:
Fields: field1,field2,field3

Create a JSON object that maps each field to a new field name by prepending 'mapped_' to the original field name.
The response should be in valid JSON format with this structure without markdown prefix or suffix:
{{
    "field_mappings": "object of key is field and valie is "mapped_<fieldname>"
}}
Reply with the JSON directly without prefixing it with any text or markdown and without any additional JSON keys like rows.

Example:
Input:

Fields: hello,foo

Output:
{{
    "field_mappings": {{ "hello": "mapped_hello", "foo": "mapped_foo" }}
}}

Your turn now,
Input:
Fields: {fields}
"""
)

@app.post("/generate-mapping", response_model=FieldMapping)
async def generate_mapping(request: FieldMappingRequest):
    try:
        # Prepare the prompt
        fields_str = request.Excel_data_fields
        prompt = MAPPING_PROMPT.format(
            fields=fields_str
        )

        # Get response from Bedrock
        response = bedrock.invoke(prompt)

        print("===========", response)
        # Parse the response
        try:
            mapping_data = json.loads(response.strip().strip("Output:").strip("output:"))
            mapping_data["Account_name"] = request.Account_name
            mapping_data["Root_directory"] = request.Root_directory

            return FieldMapping(**mapping_data)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="Failed to parse LLM response as JSON"
            )

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )
# Handler for AWS Lambda
# handler = Mangum(app)
if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=8080)