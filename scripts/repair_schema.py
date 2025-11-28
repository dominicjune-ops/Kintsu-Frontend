#!/usr/bin/env python3
"""
Schema repair script - creates a clean resume-file-schema.json with all fixes applied
"""

import json
import os

def create_clean_schema():
    """Create a clean schema with all 7 improvements"""
    
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://careercoach.ai/schemas/resume_file.schema.json",
        "title": "Resume_File",
        "description": "Schema for resume file processing and parsing with comprehensive validation and audit trail",
        "type": "object",
        "required": [
            "Resume_File_ID",
            "Candidate_ID",
            "Source",
            "Original_File_URI",
            "Mime_Type",
            "Ingested_At",
            "Parse_Status",
            "Parsing_Confidence_Score"
        ],
        "additionalProperties": False,
        "properties": {
            "Resume_File_ID": {
                "type": "string",
                "description": "Unique identifier (UUIDv4 or ULID) for the resume file",
                "oneOf": [
                    {
                        "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
                        "description": "UUIDv4 format"
                    },
                    {
                        "pattern": "^[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}$",
                        "description": "ULID format (Crockford base32)"
                    }
                ]
            },
            "Candidate_ID": {
                "type": "string",
                "description": "Reference to the candidate this resume belongs to"
            },
            "Source": {
                "type": "string",
                "enum": ["upload_web", "email_forward", "ats_import", "api"],
                "description": "Source channel where the resume was received"
            },
            "Original_File_URI": {
                "type": "string",
                "format": "uri",
                "description": "Immutable URI to the original file storage location"
            },
            "Mime_Type": {
                "type": "string",
                "enum": [
                    "application/pdf",
                    "application/msword",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "text/plain"
                ],
                "description": "MIME type of the original file"
            },
            "File_Size_Bytes": {
                "type": "integer",
                "minimum": 1,
                "maximum": 10485760,
                "description": "File size in bytes (max 10MB)"
            },
            "Checksum_SHA256": {
                "type": "string",
                "minLength": 64,
                "maxLength": 64,
                "pattern": "^[A-Fa-f0-9]{64}$",
                "description": "SHA-256 checksum for file integrity verification"
            },
            "Language": {
                "type": "string",
                "pattern": "^[a-z]{2}(-[A-Z]{2})?$",
                "description": "BCP-47 tag, e.g., en-US, es-MX"
            },
            "Ingested_At": {
                "type": "string",
                "format": "date-time",
                "description": "ISO 8601 timestamp when file was ingested"
            },
            "Parse_Status": {
                "type": "string",
                "enum": ["queued", "processing", "success", "partial", "failed"],
                "description": "Current parsing status of the resume"
            },
            "Parsing_Confidence_Score": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "description": "Confidence score (0-1) for the parsing accuracy"
            },
            "Parsed_Fields": {
                "type": "object",
                "description": "Structured data extracted from the resume",
                "additionalProperties": False,
                "properties": {
                    "Contact": {
                        "type": "object",
                        "description": "Contact information extracted from resume",
                        "additionalProperties": False,
                        "properties": {
                            "Full_Name": {
                                "type": "string",
                                "minLength": 2,
                                "maxLength": 100
                            },
                            "Email": {
                                "type": "string",
                                "format": "email"
                            },
                            "Phone": {
                                "type": "string",
                                "pattern": "^\\+?[1-9]\\d{1,14}$"
                            },
                            "Location": {
                                "type": "string",
                                "maxLength": 200
                            },
                            "LinkedIn_URL": {
                                "type": "string",
                                "format": "uri",
                                "pattern": "^https://[a-z]{2,3}\\.linkedin\\.com/"
                            },
                            "Portfolio_URL": {
                                "type": "string",
                                "format": "uri"
                            }
                        },
                        "anyOf": [
                            {"required": ["Full_Name"]},
                            {"required": ["Email"]}
                        ]
                    }
                }
            },
            "Errors": {
                "type": "array",
                "description": "Parsing errors and warnings",
                "items": {
                    "type": "object",
                    "required": ["Code", "Message", "Occurred_At"],
                    "additionalProperties": False,
                    "properties": {
                        "Code": {
                            "type": "string",
                            "pattern": "^[A-Z][A-Z0-9_]{2,20}$"
                        },
                        "Severity": {
                            "type": "string",
                            "enum": ["info", "warning", "error", "critical"]
                        },
                        "Message": {
                            "type": "string",
                            "minLength": 10,
                            "maxLength": 500
                        },
                        "Occurred_At": {
                            "type": "string",
                            "format": "date-time"
                        },
                        "Trace_ID": {
                            "type": "string",
                            "pattern": "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
                        },
                        "Payload_Snippet": {
                            "type": "string",
                            "maxLength": 1000
                        }
                    }
                }
            },
            "Audit": {
                "type": "object",
                "description": "Audit trail for compliance and versioning",
                "required": ["Created_By", "Created_At", "Version"],
                "additionalProperties": False,
                "properties": {
                    "Created_By": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 50
                    },
                    "Created_At": {
                        "type": "string",
                        "format": "date-time"
                    },
                    "Updated_By": {
                        "type": "string",
                        "maxLength": 50
                    },
                    "Updated_At": {
                        "type": "string",
                        "format": "date-time"
                    },
                    "Version": {
                        "type": "integer",
                        "minimum": 1
                    }
                }
            }
        }
    }
    
    # Write the clean schema
    try:
        # Remove existing file if it exists
        if os.path.exists('schema/resume-file-schema.json'):
            os.remove('schema/resume-file-schema.json')
            
        with open('schema/resume-file-schema.json', 'w') as f:
            json.dump(schema, f, indent=2)
        
        print(" Clean schema created successfully")
        print(" All 7 improvements applied:")
        print("  1. UUID/ULID oneOf pattern validation")
        print("  2. SHA-256 hex pattern (64 chars, A-F0-9)")
        print("  3. File size maximum (10MB = 10,485,760 bytes)")
        print("  4. Contact field anyOf requirement (Full_Name OR Email)")
        print("  5. additionalProperties: false throughout")
        print("  6. Trace_ID UUID pattern")
        print("  7. Comprehensive validation patterns")
        
        return True
        
    except Exception as e:
        print(f" Error creating schema: {e}")
        return False

if __name__ == "__main__":
    create_clean_schema()