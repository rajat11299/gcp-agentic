import os
import json
import requests # Requires 'requests' in requirements.txt

# Load OPA violations
with open('opa_violations.json', 'r') as f:
    violations = json.load(f)

# Load Terraform Plan (simplified for context)
with open('tfplan.json', 'r') as f:
    tf_plan = json.load(f)

def generate_review(violations, plan):
    if not violations.get('result'):
        return "✅ **Agent Review:** Infrastructure looks good! No policy violations found."

    # Construct Prompt for the LLM
    prompt = f"""
    You are a Senior DevOps Engineer reviewing Terraform code for GCP.
    
    1. **Strict Rules:** The following policy violations were found by OPA:
    {json.dumps(violations['result'], indent=2)}
    
    2. **Context:** Here is a summary of the resource changes:
    {json.dumps(plan['resource_changes'], indent=2)}
    
    **Task:** Write a GitHub Pull Request comment. 
    - List the blocking violations clearly.
    - Explain *why* they are dangerous in a GCP context.
    - Suggest the specific Terraform code fix for each.
    - Be empathetic but firm on security.
    """
    
    # Call LLM API (Example using generic structure)
    # Replace with your actual LLM call (Vertex AI, Gemini, OpenAI)
    # response = llm_client.generate(prompt)
    return "Dummy response: Fix your public buckets!" # Replace with actual LLM output

review_body = generate_review(violations, tf_plan)
print(review_body)

# Save for GitHub Action to use
with open('pr_comment.txt', 'w') as f:
    f.write(review_body)
