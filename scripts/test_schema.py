#!/usr/bin/env python3
import json
import jsonschema
import sys

def test_schema():
    try:
        # Load schema
        with open('schema/resume-file-schema.json', 'r') as f:
            content = f.read()
            print(f"Schema file size: {len(content)} characters")
            
        # Try to parse JSON
        schema = json.loads(content)
        print(" JSON syntax is valid")
        
        # Test schema validation
        jsonschema.Draft202012Validator.check_schema(schema)
        print(" Schema conforms to Draft 2020-12")
        
        # Test sample validation
        sample = {
            "Resume_File_ID": "550e8400-e29b-41d4-a716-446655440000",
            "Candidate_ID": "CAND123",
            "Source": "upload_web",
            "Original_File_URI": "https://storage.careercoach.ai/files/sample.pdf",
            "Mime_Type": "application/pdf",
            "Ingested_At": "2024-01-15T10:30:00Z",
            "Parse_Status": "success",
            "Parsing_Confidence_Score": 0.95
        }
        
        jsonschema.validate(sample, schema)
        print(" Sample instance validates successfully")
        
        # Test improvements
        print("\n Checking applied fixes:")
        
        # Check UUID/ULID patterns
        resume_id = schema["properties"]["Resume_File_ID"]
        if "oneOf" in resume_id:
            print(" Fix 1: UUID/ULID oneOf patterns implemented")
        else:
            print(" Fix 1: UUID/ULID patterns missing")
            
        # Check additionalProperties
        if schema.get("additionalProperties") == False:
            print(" Fix 2: Top-level additionalProperties: false")
        else:
            print(" Fix 2: Missing top-level additionalProperties: false")
            
        # Check file size limit
        file_size = schema["properties"].get("File_Size_Bytes", {})
        if file_size.get("maximum") == 10485760:
            print(" Fix 3: File size limit (10MB)")
        else:
            print(" Fix 3: File size limit not set correctly")
            
        # Check checksum pattern
        checksum = schema["properties"].get("Checksum_SHA256", {})
        if checksum.get("pattern") == "^[A-Fa-f0-9]{64}$":
            print(" Fix 4: SHA-256 hex pattern validation")
        else:
            print(" Fix 4: SHA-256 pattern incorrect")
            
        return True
        
    except json.JSONDecodeError as e:
        print(f" JSON syntax error: {e}")
        return False
    except jsonschema.SchemaError as e:
        print(f" Schema validation error: {e}")
        return False
    except Exception as e:
        print(f" Error: {e}")
        return False

if __name__ == "__main__":
    success = test_schema()
    print(f"\n{' VALIDATION PASSED' if success else ' VALIDATION FAILED'}")