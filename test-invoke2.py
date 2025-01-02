from main import MAPPING_PROMPT, bedrock

fields_str = "randomer, field1,field2,field3"
prompt = MAPPING_PROMPT.format(fields=fields_str)


print(prompt)

response = bedrock.invoke(prompt)
print(response.content)
