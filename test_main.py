"""
Unit tests for the FastAPI Token Generator API.

This module contains comprehensive tests for all API endpoints using FastAPI's TestClient.
Tests verify:
- Endpoint availability and correct status codes
- Response structure and required fields
- Data validation and error handling
"""

import pytest
from fastapi.testclient import TestClient

from main import app

# Initialize TestClient for testing
client = TestClient(app)


class TestWelcomeEndpoint:
    """Tests for the welcome endpoint (GET /)."""

    def test_welcome_status_code(self) -> None:
        """
        Test that the welcome endpoint returns a 200 status code.

        This ensures the endpoint is accessible and functioning correctly.
        """
        response = client.get("/")
        assert response.status_code == 200

    def test_welcome_response_structure(self) -> None:
        """
        Test that the welcome endpoint returns the correct response structure.

        Verifies that the response contains a 'message' field with the expected
        welcome message.
        """
        response = client.get("/")
        data = response.json()
        assert "message" in data
        assert data["message"] == "Welcome to Anuvab's Token Generator API"

    def test_welcome_content_type(self) -> None:
        """
        Test that the welcome endpoint returns JSON content type.

        Ensures proper API response format.
        """
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"


class TestChecksumEndpoint:
    """Tests for the checksum generation endpoint (POST /checksum)."""

    def test_checksum_status_code(self) -> None:
        """
        Test that the checksum endpoint returns a 200 status code for valid input.

        This confirms the endpoint successfully processes requests.
        """
        payload = {"text": "Hello, World!"}
        response = client.post("/checksum", json=payload)
        assert response.status_code == 200

    def test_checksum_response_structure(self) -> None:
        """
        Test that the checksum endpoint returns the correct response structure.

        Verifies that the response contains both 'text' and 'checksum' fields.
        """
        payload = {"text": "Hello, World!"}
        response = client.post("/checksum", json=payload)
        data = response.json()

        assert "text" in data
        assert "checksum" in data

    def test_checksum_field_exists(self) -> None:
        """
        Test that the checksum field exists in the response.

        This is a critical check to ensure the endpoint returns the expected data.
        """
        payload = {"text": "test text"}
        response = client.post("/checksum", json=payload)
        data = response.json()

        assert "checksum" in data
        assert isinstance(data["checksum"], str)
        assert len(data["checksum"]) > 0

    def test_checksum_correctness(self) -> None:
        """
        Test that the generated checksum is correct.

        Verifies the SHA256 hash is calculated accurately for known input.
        """
        import hashlib

        test_text = "Hello, World!"
        expected_checksum = hashlib.sha256(
            test_text.encode("utf-8")
        ).hexdigest()

        payload = {"text": test_text}
        response = client.post("/checksum", json=payload)
        data = response.json()

        assert data["checksum"] == expected_checksum

    def test_checksum_preserves_original_text(self) -> None:
        """
        Test that the original text is preserved in the response.

        Ensures the API returns the exact input text back to the client.
        """
        test_text = "Sample text for checksum"
        payload = {"text": test_text}
        response = client.post("/checksum", json=payload)
        data = response.json()

        assert data["text"] == test_text

    def test_checksum_different_inputs_produce_different_checksums(
        self,
    ) -> None:
        """
        Test that different inputs produce different checksums.

        This verifies the checksum function is sensitive to input changes.
        """
        payload1 = {"text": "text1"}
        payload2 = {"text": "text2"}

        response1 = client.post("/checksum", json=payload1)
        response2 = client.post("/checksum", json=payload2)

        data1 = response1.json()
        data2 = response2.json()

        assert data1["checksum"] != data2["checksum"]

    def test_checksum_same_input_produces_same_checksum(self) -> None:
        """
        Test that the same input consistently produces the same checksum.

        This verifies the checksum function is deterministic.
        """
        payload = {"text": "consistent input"}

        response1 = client.post("/checksum", json=payload)
        response2 = client.post("/checksum", json=payload)

        data1 = response1.json()
        data2 = response2.json()

        assert data1["checksum"] == data2["checksum"]

    def test_checksum_content_type(self) -> None:
        """
        Test that the checksum endpoint returns JSON content type.

        Ensures proper API response format.
        """
        payload = {"text": "test"}
        response = client.post("/checksum", json=payload)
        assert response.headers["content-type"] == "application/json"


class TestValidationErrors:
    """Tests for request validation and error handling."""

    def test_checksum_empty_text_validation(self) -> None:
        """
        Test that empty text is rejected by validation.

        The TextRequest model requires min_length=1.
        """
        payload = {"text": ""}
        response = client.post("/checksum", json=payload)
        assert response.status_code == 422

    def test_checksum_missing_text_field(self) -> None:
        """
        Test that missing the 'text' field returns a validation error.

        The 'text' field is required in the TextRequest model.
        """
        payload = {}
        response = client.post("/checksum", json=payload)
        assert response.status_code == 422

    def test_checksum_text_field_not_string(self) -> None:
        """
        Test that non-string values for 'text' field are rejected.

        The 'text' field must be a string.
        """
        payload = {"text": 123}
        response = client.post("/checksum", json=payload)
        assert response.status_code == 422

    def test_checksum_extra_fields_ignored(self) -> None:
        """
        Test that extra fields in the request are handled gracefully.

        Pydantic should ignore extra fields by default.
        """
        payload = {"text": "test", "extra_field": "value"}
        response = client.post("/checksum", json=payload)
        assert response.status_code == 200


class TestIntegration:
    """Integration tests for the complete API."""

    def test_api_workflow(self) -> None:
        """
        Test a complete API workflow.

        1. Check welcome endpoint is available
        2. Generate a checksum
        3. Verify the response structure
        """
        # Check welcome
        welcome_response = client.get("/")
        assert welcome_response.status_code == 200

        # Generate checksum
        payload = {"text": "integration test"}
        checksum_response = client.post("/checksum", json=payload)
        assert checksum_response.status_code == 200

        # Verify response
        data = checksum_response.json()
        assert data["text"] == "integration test"
        assert "checksum" in data
        assert len(data["checksum"]) == 64  # SHA256 produces 64 hex characters


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
