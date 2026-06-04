# Anuvab's Token Generator API

A production-ready FastAPI application for generating SHA256 checksums and managing text processing operations.

## 🚀 Features

- **Welcome Endpoint**: Simple health check endpoint
- **Checksum Generation**: Generate SHA256 checksums for input text
- **Comprehensive Documentation**: Swagger UI and ReDoc automatically generated
- **Type Safety**: Full Pydantic model validation
- **Production Ready**: Following FastAPI best practices with proper error handling
- **Fully Tested**: Comprehensive unit test suite with high coverage
- **Well Documented**: Detailed docstrings and comments throughout

## 📋 Project Overview

This API provides two main endpoints:

1. **GET `/`** - Welcome endpoint that returns a greeting message
2. **POST `/checksum`** - Generates SHA256 checksums for provided text

The application uses:
- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **Uvicorn** - Fast ASGI server for running the application
- **Pytest** - Testing framework for unit tests

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/anuvab03/fastapi-token-generator.git
cd fastapi-token-generator
