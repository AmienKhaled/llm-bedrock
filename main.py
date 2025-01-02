import json
import os
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain.prompts import PromptTemplate
from langchain_aws import BedrockLLM, ChatBedrock
from mangum import Mangum
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Field Mapping Service")
handler = Mangum(app)

# Initialize Bedrock client
bedrock = ChatBedrock(
    credentials_profile_name="default",
    # model_id=BEDROCK_CONFIG["model_id"],
    model_id=os.getenv("MODEL_ID"),
    region_name=os.getenv("AWS_REGION", "eu-west-2"),
    temperature=0,
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
    "field_mappings": {{ "field1": "mapped_field1", "field2": "mapped_field2", "field3": "mapped_field3" }}
}}
Reply with the JSON formatted strong directly without prefixing it with any text or markdown and without any additional JSON keys like rows.

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
""",
)


@app.post("/generate-mapping", response_model=FieldMapping)
async def generate_mapping(request: FieldMappingRequest):
    try:
        # Prepare the prompt
        fields_str = ",".join(request.Excel_data_fields)
        prompt = MAPPING_PROMPT.format(fields=fields_str)

        # Get response from Bedrock
        response = bedrock.invoke(prompt)
        response = response.content
        print("==========zz", response)
        # Parse the response
        if not response:
            raise HTTPException(
                status_code=500, detail="No response received from Bedrock LLM"
            )

        try:
            mapping_data = json.loads(response.strip())
            mapping_data["Account_name"] = request.Account_name
            mapping_data["Root_directory"] = request.Root_directory
            return FieldMapping(**mapping_data)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse LLM response as JSON: {str(e)}",
            )

    except Exception as e:
        print(f"Error: {str(e)}")  # Log full error for debugging
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
