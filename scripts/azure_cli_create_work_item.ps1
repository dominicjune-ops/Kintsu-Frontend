# Azure CLI Script to Create Work Items with Default Child Tasks
# Converted to PowerShell for Windows compatibility

param(
    [Parameter(Mandatory=$true)]
    [string]$Type,  # Epic, Feature, User Story, Bug, Task

    [Parameter(Mandatory=$true)]
    [string]$Title  # e.g., "Resume Parser Feature"
)

# === CONFIG ===
$ORG_URL = "https://dev.azure.com/CareerCoachai"
$PROJECT = "CareerCoach.ai"

# === TASK TEMPLATES ===
$tasks = @{
    "Epic" = "Define strategic goals and success metrics|Break down into features and user stories|Align with product roadmap|Review with executive stakeholders|Assign responsible teams|Track progress across sprints|Document cross-team dependencies"
    "Feature" = "Clarify feature scope and user impact|Design UI/UX wireframes|Define technical architecture|Estimate effort and assign team|Create supporting user stories|Validate with product owner|Prepare release notes"
    "User Story" = "Write detailed acceptance criteria|Design UI mockups or flow diagrams|Implement core functionality|Write unit and integration tests|Conduct peer code review|Demo to stakeholders|Close after validation"
    "Bug" = "Reproduce issue and capture logs|Identify root cause|Fix and test locally|Deploy to test environment|Validate fix with QA|Close after confirmation"
    "Task" = "Clarify task objective|Assign responsible team member|Estimate effort and timeline|Execute task|Document outcome|Mark as complete"
}

# === CREATE PARENT WORK ITEM ===
$parentId = az boards work-item create --title "$Title" --type "$Type" --project "$PROJECT" --org "$ORG_URL" --query "id" -o tsv

Write-Host "Created $Type with ID: $parentId"

# === CREATE AND LINK CHILD TASKS ===
$taskList = $tasks[$Type] -split '\|'
foreach ($task in $taskList) {
    $childId = az boards work-item create --title "$task" --type "Task" --project "$PROJECT" --org "$ORG_URL" --fields "System.Tags=DefaultTask" --query "id" -o tsv

    az boards work-item relation add --id $parentId --relation-type "System.LinkTypes.Hierarchy-Forward" --target-id $childId --org "$ORG_URL" --project "$PROJECT"

    Write-Host "Linked task '$task' (ID: $childId) to $Type $parentId"
}