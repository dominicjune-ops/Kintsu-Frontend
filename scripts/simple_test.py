import json

# Test JSON validity
try:
    with open('schema/resume-file-schema.json', 'r') as f:
        schema = json.load(f)
    
    print("JSON is valid!")
    print(f"Schema title: {schema.get('title')}")
    print(f"Required fields: {len(schema.get('required', []))}")
    
    # Check for our fixes
    resume_id = schema["properties"]["Resume_File_ID"]
    print(f"Resume_File_ID has oneOf: {'oneOf' in resume_id}")
    print(f"Top-level additionalProperties: {schema.get('additionalProperties')}")
    
except Exception as e:
    print(f"Error: {e}")