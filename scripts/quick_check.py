import json
import sys

try:
    with open('schema/resume-file-schema.json', 'r') as f:
        schema = json.load(f)
    
    print("SCHEMA VALIDATION SUMMARY")
    print("=" * 30)
    print(f" JSON syntax valid")
    print(f" Schema title: {schema.get('title')}")
    print(f" Required fields: {len(schema.get('required', []))}")
    
    # Check key improvements
    improvements = []
    
    # 1. UUID/ULID patterns
    resume_id = schema["properties"]["Resume_File_ID"]
    if "oneOf" in resume_id:
        improvements.append(" UUID/ULID oneOf patterns")
    else:
        improvements.append(" UUID/ULID patterns missing")
    
    # 2. additionalProperties 
    if schema.get("additionalProperties") == False:
        improvements.append(" additionalProperties: false")
    else:
        improvements.append(" additionalProperties not set")
    
    # 3. File size limit
    file_size = schema["properties"].get("File_Size_Bytes", {})
    if file_size.get("maximum") == 10485760:
        improvements.append(" 10MB file size limit")
    else:
        improvements.append(" File size limit missing")
    
    # 4. SHA-256 pattern
    checksum = schema["properties"].get("Checksum_SHA256", {})
    if "A-Fa-f0-9" in checksum.get("pattern", ""):
        improvements.append(" SHA-256 hex pattern")
    else:
        improvements.append(" SHA-256 pattern missing")
    
    print("\nIMPROVEMENTS APPLIED:")
    for imp in improvements:
        print(imp)
    
    passed = all("" in imp for imp in improvements)
    print(f"\nOVERALL: {' PASSED' if passed else ' FAILED'}")
    
except Exception as e:
    print(f" Error: {e}")
    sys.exit(1)