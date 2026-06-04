"""
FastAPI application for generating checksums and token operations.

This module implements a production-ready API with:
- Welcome endpoint for health checks
- Checksum generation endpoint using SHA256
- Comprehensive API documentation via Swagger UI
"""

import hashlib
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Initialize FastAPI application with metadata for Swagger UI
app = FastAPI(
    title="Anuvab's Token Generator API",
    description="A production-ready API for text processing and checksum generation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# ============================================================================
# Pydantic Models
# ============================================================================


class TextRequest(BaseModel):
    """
    Request model for text input.

    Attributes:
        text (str): The input text to process. Must not be empty.

    Example:
        {
            "text": "Hello, World!"
        }
    """

    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The text to generate a checksum for",
        example="Hello, World!",
    )

    class Config:
        """Pydantic configuration for schema examples."""

        json_schema_extra = {
            "example": {"text": "Sample text for checksum generation"}
        }


class ChecksumResponse(BaseModel):
    """
    Response model for checksum endpoint.

    Attributes:
        text (str): The original input text.
        checksum (str): The SHA256 checksum of the input text.

    Example:
        {
            "text": "Hello, World!",
            "checksum": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
        }
    """

    text: str = Field(
        ..., description="The original input text"
    )
    checksum: str = Field(
        ..., description="SHA256 checksum of the input text"
    )

    class Config:
        """Pydantic configuration for schema examples."""

        json_schema_extra = {
            "example": {
                "text": "Hello, World!",
                "checksum": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f",
            }
        }


# ============================================================================
# Endpoints
# ============================================================================


@app.get(
    "/",
    tags=["Health Check"],
    summary="Welcome endpoint",
)
async def welcome() -> dict[str, str]:
    """
    Welcome endpoint for API health check.

    Returns:
        dict: A welcome message indicating the API is running.

    Example:
        GET /
        Response: {"message": "Welcome to Anuvab's Token Generator API"}
    """
    return {"message": "Welcome to Anuvab's Token Generator API"}


@app.post(
    "/checksum",
    response_model=ChecksumResponse,
    tags=["Text Processing"],
    summary="Generate SHA256 checksum",
    responses={
        200: {
            "description": "Checksum generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "text": "Hello, World!",
                        "checksum": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f",
                    }
                }
            },
        },
        422: {"description": "Validation error - invalid request body"},
    },
)
async def generate_checksum(request: TextRequest) -> ChecksumResponse:
    """
    Generate a SHA256 checksum for the provided text.

    This endpoint accepts a text string and returns its SHA256 checksum along
    with the original text for reference.

    Args:
        request (TextRequest): The request body containing the text to checksum.

    Returns:
        ChecksumResponse: A response containing the original text and its SHA256 checksum.

    Raises:
        HTTPException: If text processing fails (unlikely in normal operation).

    Example:
        POST /checksum
        Request: {"text": "Hello, World!"}
        Response: {
            "text": "Hello, World!",
            "checksum": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
        }
    """
    try:
        # Generate SHA256 hash of the input text
        checksum: str = hashlib.sha256(
            request.text.encode("utf-8")
        ).hexdigest()

        return ChecksumResponse(
            text=request.text,
            checksum=checksum,
        )
    except Exception as e:
        # Handle unexpected errors gracefully
        raise HTTPException(
            status_code=500,
            detail=f"Error generating checksum: {str(e)}",
        ) from e


if __name__ == "__main__":
    import uvicorn

    # Run the application with uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
