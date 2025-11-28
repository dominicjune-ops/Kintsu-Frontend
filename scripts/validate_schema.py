#!/usr/bin/env python3
"""
Schema validation script for Resume_File schema
Validates JSON Schema Draft 2020-12 compliance and tests sample instances
"""

import json
import jsonschema
from jsonschema import validate, Draft202012Validator
import sys
from datetime import datetime

def validate_schema():
    """Validate the resume file schema and test with sample instances"""
    
    # Load the schema
    try:
        with open('schema/resume-file-schema.json', 'r') as f:
            schema = json.load(f)
        print(" Schema loaded successfully")
    except json.JSONDecodeError as e:
        print(f" JSON syntax error in schema: {e}")
        return False
    except FileNotFoundError:
        print(" Schema file not found")
        return False
    
    # Validate schema syntax with Draft 2020-12
    try:
        Draft202012Validator.check_schema(schema)
        print(" Schema passes JSON Schema Draft 2020-12 validation")
    except jsonschema.SchemaError as e:
        print(f" Schema validation error: {e}")
        return False
    
    # Test sample valid instance
    valid_sample = {
        "Resume_File_ID": "550e8400-e29b-41d4-a716-446655440000",  # UUIDv4
        "Candidate_ID": "CAND123",
        "Source": "upload_web",
        "Original_File_URI": "https://storage.careercoach.ai/files/sample.pdf",
        "Mime_Type": "application/pdf",
        "File_Size_Bytes": 1024000,
        "Checksum_SHA256": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
        "Language": "en-US",
        "Ingested_At": "2024-01-15T10:30:00Z",
        "Parse_Status": "success",
        "Parsing_Confidence_Score": 0.95,
        "Parsed_Fields": {
            "Contact": {
                "Full_Name": "John Doe",
                "Email": "john@example.com"
            }
        },
        "Audit": {
            "Created_By": "system",
            "Created_At": "2024-01-15T10:30:00Z",
            "Version": 1
        }
    }
    
    # Test ULID format
    ulid_sample = valid_sample.copy()
    ulid_sample["Resume_File_ID"] = "01ARZ3NDEKTSV4RRFFQ69G5FAV"  # ULID
    
    # Test validation
    try:
        validate(instance=valid_sample, schema=schema)
        print(" UUIDv4 sample validates successfully")
    except jsonschema.ValidationError as e:
        print(f" UUIDv4 sample validation failed: {e}")
        return False
    
    try:
        validate(instance=ulid_sample, schema=schema)
        print(" ULID sample validates successfully")
    except jsonschema.ValidationError as e:
        print(f" ULID sample validation failed: {e}")
        return False
    
    # Test invalid instances
    invalid_samples = [
        # Invalid Resume_File_ID
        {**valid_sample, "Resume_File_ID": "invalid-id"},
        # Missing required field
        {k: v for k, v in valid_sample.items() if k != "Candidate_ID"},
        # Invalid file size (too large)
        {**valid_sample, "File_Size_Bytes": 20000000},  # 20MB > 10MB max
        # Invalid checksum
        {**valid_sample, "Checksum_SHA256": "short"},
        # Invalid MIME type
        {**valid_sample, "Mime_Type": "application/unknown"}
    ]
    
    invalid_count = 0
    for i, invalid_sample in enumerate(invalid_samples):
        try:
            validate(instance=invalid_sample, schema=schema)
            print(f" Invalid sample {i+1} unexpectedly passed validation")
            invalid_count += 1
        except jsonschema.ValidationError:
            print(f" Invalid sample {i+1} correctly rejected")
    
    if invalid_count > 0:
        print(f" {invalid_count} invalid samples passed when they should have been rejected")
        return False
    
    # Summary
    print("\n All validation tests passed!")
    print(" Schema conforms to JSON Schema Draft 2020-12")
    print(" UUIDv4 and ULID patterns work correctly")
    print(" File size limits enforced (10MB max)")
    print(" SHA-256 checksum pattern validation works")
    print(" MIME type restrictions enforced")
    print(" Required fields validation works")
    
    return True

if __name__ == "__main__":
    success = validate_schema()
    sys.exit(0 if success else 1)