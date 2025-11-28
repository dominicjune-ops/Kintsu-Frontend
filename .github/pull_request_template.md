# CareerCoach.ai Pull Request Template

## ✅ **Canonical Validation Checklist** (Required for ALL Connectors)

### **1. Schema Compliance** 
- [ ] **Required Fields Present**: All mandatory fields (`job_id`, `title`, `company_name`, `location`, `posted_date`, `apply_url`) populated
- [ ] **Field Types Match**: Data types align with canonical schema (string, date, enum, object)  
- [ ] **Location Normalized**: `location` structured as `{city, state, country, remote_flag}`
- [ ] **Date Standardized**: `posted_date` converted to UTC ISO 8601 format

### **2. Data Quality**
- [ ] **Title Cleaned**: No ALL CAPS, removed "Now Hiring" spam phrases, proper case applied
- [ ] **Company Normalized**: `company_name` standardized (no duplicates like "Microsoft Inc." vs "Microsoft")
- [ ] **URL Validated**: `apply_url` returns 200 OK status and resolves correctly  
- [ ] **Description Clean**: Generated `description_clean` from `description_raw` (HTML stripped, normalized)

### **3. Enrichment Pipeline**
- [ ] **Salary Parsed**: Structured `{min, max, currency, period}` extracted from text if available
- [ ] **Skills Extracted**: NLP pipeline identifies relevant skills from job description
- [ ] **Experience Level**: Derived classification (Entry/Mid/Senior/Executive) based on requirements
- [ ] **Intelligence Score**: Computed job relevance/quality score (0-1 scale)

### **4. Governance & Audit**
- [ ] **Deduplication Check**: Verified against existing records (`title+company_id+location+posted_date` hash)
- [ ] **Raw Payload Stored**: Original source data preserved for audit trail and reprocessing
- [ ] **Error Handling**: Failed jobs logged with retry logic or quarantine routing configured
- [ ] **Source Attribution**: `source` field correctly identifies data origin (linkedin/indeed/ziprecruiter/etc.)

## 🔗 **Connector-Specific Validation** (Check Applicable)

### **LinkedIn Connector** (if applicable)
- [ ] **Company ID Mapping**: `companyId` correctly mapped to `company_id` 
- [ ] **Employment Type**: `employmentType` normalized to canonical enum values (full_time, part_time, contract, etc.)
- [ ] **Salary Extraction**: LinkedIn salary objects transformed to canonical `salary_range` structure
- [ ] **Remote Detection**: `workRemoteAllowed` boolean mapped to `remote_flag` correctly

### **Indeed Connector** (if applicable)  
- [ ] **Job Key Mapping**: `jobkey` correctly mapped to canonical `job_id`
- [ ] **Salary Parsing**: Text salary ("$X - $Y per year") parsed into structured `salary_range`
- [ ] **Location Parsing**: `formattedLocation` correctly split into city/state/country components
- [ ] **Date Conversion**: Indeed date formats standardized to UTC timestamps

### **ZipRecruiter Connector** (if applicable)
- [ ] **Salary Range**: `salary_min`/`salary_max` correctly combined into `salary_range` object
- [ ] **Company Name**: `hiring_company.name` properly extracted and normalized
- [ ] **Location Handling**: ZipRecruiter location strings parsed and standardized
- [ ] **Employment Type**: ZipRecruiter job types mapped to canonical employment enum

### **Google Jobs Connector** (if applicable)
- [ ] **Date Parsing**: `datePosted` correctly converted to UTC ISO 8601
- [ ] **API Compliance**: Adheres to Google Custom Search API Terms of Service
- [ ] **Result Filtering**: Non-job results filtered out from search responses  
- [ ] **URL Extraction**: Original job posting URLs correctly preserved

### **Bing Jobs Connector** (if applicable)
- [ ] **Provider Mapping**: `provider.name` correctly mapped to `company_name`
- [ ] **Date Standardization**: `datePublished` parsed into UTC format
- [ ] **Content Quality**: Bing job descriptions cleaned and normalized
- [ ] **Duplicate Detection**: Bing-specific deduplication logic applied

## ⚙️ **Cross-Platform Integration Verification**

### **Azure DevOps Pipeline**
- [ ] **Schema Validation Step**: Added/updated build step to validate canonical compliance  
- [ ] **Pipeline Fails Fast**: Build fails if validation checklist requirements not met
- [ ] **Test Coverage**: Integration tests cover new connector functionality end-to-end
- [ ] **Deployment Gates**: Validation requirements included in release approval process

### **GitHub Integration**  
- [ ] **PR Template**: This checklist completed and verified by reviewers before merge
- [ ] **Branch Protection**: Required status checks enforce validation pipeline completion
- [ ] **Review Requirements**: Minimum 2 approvals for connector changes, schema team approval for breaking changes
- [ ] **Issue Linking**: Related issues/user stories linked to this connector update

### **Notion Database**
- [ ] **Validation Status Property**: "Pass/Fail" property tracks validation compliance per job record
- [ ] **Schema Alignment**: Notion database structure reflects canonical field mappings
- [ ] **Views Updated**: Connector-specific views show data quality and validation metrics
- [ ] **Audit Trail**: Notion pages link to source validation records and raw payloads

### **Zapier/Make.com Automation**
- [ ] **Validation Routing**: Failed validation triggers quarantine workflow (separate database + Slack alert)
- [ ] **Success Path**: Validated jobs flow to main processing pipeline automatically  
- [ ] **Error Handling**: Retry logic configured for temporary validation failures
- [ ] **Monitoring**: Zapier automation tracks validation success rates and alerts on degradation

### **MS Project Tracking**
- [ ] **Validation Milestone**: Connector rollout includes validation checklist as deliverable milestone
- [ ] **Progress Tracking**: Validation compliance tracked as project KPI across all connectors
- [ ] **Resource Planning**: Validation effort estimated and allocated in project timeline
- [ ] **Risk Management**: Validation failure scenarios included in project risk register

### **VS Code Development**
- [ ] **JSON Schema Validation**: Local development uses schema validation extension for real-time feedback
- [ ] **Pre-commit Hooks**: Git hooks run validation checklist before allowing commit  
- [ ] **Debug Configuration**: VS Code debugger configured to step through validation pipeline
- [ ] **Task Runner**: VS Code tasks configured for running validation scripts locally

## 🧪 **Technical Validation**

### **Schema Validation Results**
- [ ] **JSON Schema Syntax**: All schema files validate as proper JSON Schema Draft 7
- [ ] **Reference Resolution**: All `$ref` references resolve correctly to canonical schema
- [ ] **Sample Data Tests**: Test data validates successfully against updated schemas
- [ ] **Backward Compatibility**: Schema changes don't break existing data or workflows
- [ ] **Performance Impact**: Changes don't negatively impact connector or enrichment performance

### **Code Quality Checks**
- [ ] **Pre-commit Hooks**: All pre-commit validation hooks pass locally
- [ ] **Unit Test Coverage**: Maintained >80% test coverage for affected components
- [ ] **Integration Tests**: End-to-end connector → queue → enrichment tests pass
- [ ] **Linting Standards**: Code follows project style guidelines (black, pylint)
- [ ] **Security Scan**: No new security vulnerabilities introduced

## 🚀 **Deployment Readiness**

### **Infrastructure Requirements**  
- [ ] **Environment Variables**: Required environment variables documented/configured
- [ ] **Dependencies**: Any new dependencies added to requirements.txt
- [ ] **Container Updates**: Container configurations updated if needed
- [ ] **Monitoring Setup**: Application Insights/monitoring configured for new components
- [ ] **Rollback Plan**: Rollback procedure documented for this change

### **Documentation Updates**
- [ ] **README Updates**: README.md updated with new features/requirements  
- [ ] **API Documentation**: API changes documented in relevant files
- [ ] **Field Mapping Docs**: FIELD_MAPPING.md updated for connector changes
- [ ] **Integration Guide**: archive/deprecated/INTEGRATION_GUIDE.md updated for workflow changes
- [ ] **Compliance Checklists**: COMPLIANCE_CHECKLISTS.md updated if needed

## 🔍 **Testing Evidence**

#### **Validation Commands Run** (Paste Output)
```powershell
# Canonical validation checklist (REQUIRED - paste full output)
python scripts/validate_compliance.py --mode connectors --connector [connector_name]

# Schema compliance verification  
python -c "import json, jsonschema, glob; [jsonschema.Draft7Validator.check_schema(json.load(open(f))) for f in glob.glob('schema/*-schema.json')]"

# Connector-specific tests
python -m pytest tests/connectors/test_[connector_name]_connector.py -v --tb=short

# End-to-end validation pipeline
python -m pytest tests/integration/ -k "test_canonical_validation" -v
```

#### **Validation Results Summary**
```
Schema Validation: ✅ PASS / ❌ FAIL  
Data Quality Check: ✅ PASS / ❌ FAIL
Enrichment Pipeline: ✅ PASS / ❌ FAIL  
Governance & Audit: ✅ PASS / ❌ FAIL
Connector-Specific: ✅ PASS / ❌ FAIL
Integration Verification: ✅ PASS / ❌ FAIL

Overall Validation Status: ✅ COMPLIANT / ❌ NON-COMPLIANT
```

### **Manual Testing Completed**
- [ ] **Connector Output**: Manually tested connector with sample data  
- [ ] **Queue Processing**: Verified message processing through Service Bus
- [ ] **Enrichment Service**: Tested data enrichment and canonical validation
- [ ] **Notion Integration**: Verified data appears correctly in Notion database
- [ ] **Zapier Automation**: Tested automation workflows with new data structure

## 👥 **Review Requirements**

### **Required Reviewers**
- [ ] **Schema Team**: @schema-team (required for schema changes)
- [ ] **DevOps Team**: @devops-team (required for infrastructure changes)
- [ ] **QA Team**: @qa-team (required for connector changes)

### **Approval Criteria**
- [ ] **Minimum 2 Approvals**: Required for schema or breaking changes
- [ ] **1 Approval**: Sufficient for documentation/minor updates  
- [ ] **Schema Lead Approval**: Required for canonical-schema.json changes
- [ ] **Security Review**: Required for authentication/API changes

---

## **Change Description**

### **Summary**
<!-- Brief description of what this PR accomplishes -->

### **Motivation**  
<!-- Why is this change needed? Link to issues/requirements -->

### **Changes Made**
<!-- Detailed list of files changed and what was modified -->

### **Testing Strategy**
<!-- How was this change tested? Include test scenarios -->

### **Rollback Plan**
<!-- How would you rollback this change if issues arise? -->

---

## **Additional Notes**

### **Breaking Changes** ⚠️  
<!-- List any breaking changes and migration requirements -->

### **Performance Impact** 📊
<!-- Document any performance implications -->

### **Security Considerations** 🔒
<!-- Note any security-related changes or considerations -->

### **Dependencies** 📦
<!-- List any new dependencies or version updates -->

---

**Reviewer Guidelines**: 
- Verify all checklists are completed before approval
- Test changes locally using provided validation commands  
- Ensure documentation is clear and complete
- Confirm rollback plan is feasible and documented