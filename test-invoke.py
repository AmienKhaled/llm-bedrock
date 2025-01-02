import requests

url = "http://0.0.0.0:8080/generate-mappings"
headers = {"Content-Type": "application/json"}
data = {
    "Account_name": "TestAccount",
    "Root_directory": "test_dir",
    "Excel_data_fields": ["field1", "field2"],
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
