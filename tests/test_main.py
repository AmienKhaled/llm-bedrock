from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

def test_generate_mapping_valid_request():
    test_request = {
        "Account_name": "test_account",
        "Root_directory": "test_directory",
        "Excel_data_fields": ["field1", "field2"]
    }

    response = client.post("/generate-mapping", json=test_request)
    assert response.status_code == 200

    data = response.json()
    assert "Account_name" in data
    assert "Root_directory" in data
    assert "field_mappings" in data

    # Verify field mappings
    field_mappings = data["field_mappings"]
    for field in test_request["Excel_data_fields"]:
        assert field in field_mappings
        assert field_mappings[field].startswith("mapped_")

def test_generate_mapping_invalid_request():
    # Missing required field
    test_request = {
        "Account_name": "test_account",
        "Root_directory": "test_directory"
        # Missing Excel_data_fields
    }

    response = client.post("/generate-mapping", json=test_request)
    assert response.status_code == 422  # Validation error

def test_generate_mapping_empty_fields():
    test_request = {
        "Account_name": "test_account",
        "Root_directory": "test_directory",
        "Excel_data_fields": []
    }

    response = client.post("/generate-mapping", json=test_request)
    assert response.status_code == 200
    data = response.json()
    assert data["field_mappings"] == {}