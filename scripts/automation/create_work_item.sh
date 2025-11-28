#!/bin/bash

# === CONFIG ===
ORG_URL="https://dev.azure.com/CareerCoachai"
PROJECT="CareerCoach.ai"
TYPE="$1"  # Epic, Feature, User Story, Bug, Task
TITLE="$2" # e.g., "Resume Parser Feature"

# === TASK TEMPLATES ===
declare -A TASKS

TASKS["Epic"]="Define strategic goals and success metrics|Break down into features and user stories|Align with product roadmap|Review with executive stakeholders|Assign responsible teams|Track progress across sprints|Document cross-team dependencies"

TASKS["Feature"]="Clarify feature scope and user impact|Design UI/UX wireframes|Define technical architecture|Estimate effort and assign team|Create supporting user stories|Validate with product owner|Prepare release notes"

TASKS["User Story"]="Write detailed acceptance criteria|Design UI mockups or flow diagrams|Implement core functionality|Write unit and integration tests|Conduct peer code review|Demo to stakeholders|Close after validation"

TASKS["Bug"]="Reproduce issue and capture logs|Identify root cause|Fix and test locally|Deploy to test environment|Validate fix with QA|Close after confirmation"

TASKS["Task"]="Clarify task objective|Assign responsible team member|Estimate effort and timeline|Execute task|Document outcome|Mark as complete"

# === CREATE PARENT WORK ITEM ===
PARENT_ID=$(az boards work-item create \
  --title "$TITLE" \
  --type "$TYPE" \
  --project "$PROJECT" \
  --org "$ORG_URL" \
  --query "id" -o tsv)

echo "Created $TYPE with ID: $PARENT_ID"

# === CREATE AND LINK CHILD TASKS ===
IFS='|' read -ra ITEMS <<< "${TASKS[$TYPE]}"
for TASK in "${ITEMS[@]}"; do
  CHILD_ID=$(az boards work-item create \
    --title "$TASK" \
    --type "Task" \
    --project "$PROJECT" \
    --org "$ORG_URL" \
    --fields "System.Tags=DefaultTask" \
    --query "id" -o tsv)

  az boards work-item relation add \
    --id $PARENT_ID \
    --relation-type "System.LinkTypes.Hierarchy-Forward" \
    --target-id $CHILD_ID \
    --org "$ORG_URL" \
    --project "$PROJECT"

  echo "Linked task '$TASK' (ID: $CHILD_ID) to $TYPE $PARENT_ID"
done