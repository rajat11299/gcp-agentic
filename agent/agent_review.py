import os
import json
import re

def generate_review(violations, plan):
    """
    Generates a GitHub PR comment based on OPA violations.
    """
    # Check if 'result' key exists and has content
    if not violations.get('result'):
        return "✅ **Agent Review:** Infrastructure looks good! No policy violations found."

    # Parse violations
    violation_messages = []
    # OPA output structure: violations['result'][0]['expressions'][0]['value'] is a list of strings
    try:
        # Access the first result's first expression's value
        if violations['result'] and violations['result'][0].get('expressions'):
            violation_messages = violations['result'][0]['expressions'][0]['value']
    except (KeyError, IndexError, TypeError):
        # Fallback if structure is unexpected
        return "⚠️ **Agent Review:** Errors found but could not parse details. Please check the OPA logs for raw output."
    
    if not violation_messages:
         return "✅ **Agent Review:** Infrastructure looks good! No policy violations found."

    # Build Markdown Report
    report = ["### 🛑 Policy Violations Detected\n"]
    report.append(f"**Total Violations:** {len(violation_messages)}\n")
    
    # Table Header
    report.append("| Category | Message | Resource |")
    report.append("| :--- | :--- | :--- |")
    
    for msg in violation_messages:
        # Expected msg format: "category: message text." or similar
        # Based on rego: "security-risk: Bucket '...' must have uniform..."
        parts = msg.split(':', 1)
        category = parts[0].strip() if len(parts) > 1 else "General"
        message_body = parts[1].strip() if len(parts) > 1 else msg
        
        # Extract resource name if possible (heuristic: quoted in single quotes)
        resource_match = re.search(r"'([^']*)'", message_body)
        resource = resource_match.group(1) if resource_match else "Unknown"
        
        # Escape pipe characters in message to avoid breaking markdown table
        safe_message = message_body.replace("|", "\\|")
        
        report.append(f"| **{category}** | {safe_message} | `{resource}` |")

    report.append("\nPLEASE FIX THE ABOVE ISSUES TO PROCEED.")
    
    return "\n".join(report)

if __name__ == "__main__":
    # Load OPA violations
    try:
        with open('opa_violations.json', 'r') as f:
            violations = json.load(f)
    except FileNotFoundError:
        print("Error: opa_violations.json not found.")
        violations = {}

    # Load Terraform Plan (simplified for context)
    try:
        with open('tfplan.json', 'r') as f:
            tf_plan = json.load(f)
    except FileNotFoundError:
        print("Error: tfplan.json not found.")
        tf_plan = {}

    review_body = generate_review(violations, tf_plan)
    print(review_body)

    # Save for GitHub Action to use
    with open('pr_comment.txt', 'w', encoding='utf-8') as f:
        f.write(review_body)
