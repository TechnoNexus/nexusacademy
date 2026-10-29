import json
from collections import defaultdict
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('pega_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

from create_28_questions import new_questions

FIXES_ZERO = {
    18: 1,  # Automatic Promotion: "No action is required."
    28: 2,  # Table vs. Tree Selection: "Decision Tree"
    38: 2,  # Action vs. Process: "Add an Optional Process."
    39: 1,  # Determining the Scope: "Configure a Stage-only Optional Action in the Underwriting Stage."
    43: 2,  # Developer Productivity: "Low-code tools allow professional developers to build and extend robust applications..."
    47: 1,  # The Architect's Workspace: "App Studio, to reduce potential errors and auto-generate rules."
    50: 1,  # Differentiating the Model and the Instance: "A Case"
    67: 3,  # Private Development Space: "In their personal Workspace"
    72: 1,  # Reaching the Threshold: "The case is NOT flagged as a potential duplicate."
    83: 1,  # Timing of the Validation: "Validation on a Stage."
    84: 1,  # Immediate Correction: "Validation on a Form."
    92: 2,  # Manipulating Data in Transit: "On the Connector properties between the Review and Approval shapes."
    103: 2, # The "Older Than" Timing Trap: "10:00 AM"
    107: 2, # Always Up-to-Date: "Refer to a Data Page"
    108: 1, # The Display vs Value Configuration: "Set the Property for display text to the Currency Name..."
    116: 1, # Implicit Parameter Passing: "In the Property Rule form for EmployeeRecord."
    121: 1, # Authentication vs. Authorization: "Authorization"
    124: 1, # Differentiating Security Levels: "Feature security"
    125: 2, # The Operator Disablement Exception: "Add the SysAdmin operator ID to the Exclusion list..."
    130: 3, # Single Sign-On: "Authentication (Specifically SSO using SAML/OpenID)"
    140: 1, # Custom Condition vs. When Rule: "Use a When Rule and apply it to all three screens."
    142: 1, # Conditional Requirements: "Required = Custom Condition (If Preferred Method == Email)"
}

ENRICH_EXPLANATIONS = {
    87: "A Validate rule can qualify validation conditions based on the Proposed Work Status, allowing different validation requirements to execute depending on what status the case will transition into.",
    95: "In class inheritance, when the same property is set in both a parent class and a subclass data transform, the subclass value takes precedence and overrides the parent class value.",
    102: "Checking 'Limit to a single Data Page' ensures that only one instance of the parameterized data page exists on the clipboard at any given time, recycling memory and preventing memory bloat when iterating through many parameter values.",
    106: "When data must reflect a snapshot in time that should never change even if external master records change later (such as policy coverage terms at the time an insurance claim was filed), you should copy data from a Data Page rather than referring to it.",
    115: "A Data Transform can initialize new page structures and calculate or populate required key properties prior to persistence, avoiding missing key errors.",
    117: "When you specify the Savable Data Page explicitly by name in the Save Data Page step, Pega saves the specific instance directly without needing it to be associated with an embedded property.",
    122: "Writing custom Java code for security credentials introduces severe maintenance and security vulnerabilities and violates Pega Guardrails. Pega Platform includes standard authentication and password policy configurations out of the box.",
    127: "Security, access roles, and personas must be designed and architected early during the Prepare phase of Pega Express delivery, rather than treated as an afterthought near go-live.",
    135: "A Persona represents a business user perspective and the experiences they have in the application, while an Access Role defines the technical permissions and authorizations granted to perform operations on specific classes.",
    137: "Access Deny records explicitly prohibit access regardless of permissions granted by other roles in the user's access group, ensuring strict compliance.",
    139: "Pega strongly recommends managing access using the Access Manager or Persona security settings in App Studio, as manual modifications to Access of Role to Object (ARO) rule forms can lead to inconsistencies and upgrade difficulties.",
    147: "External end users who submit service requests or view account details require a streamlined, responsive Self-service Portal rather than a back-office casework portal.",
    148: "In Pega Constellation and Cosmos portals, business dashboards and metric reports are added as Landing Pages in the portal navigation menu.",
    149: "Instead of creating redundant portals, best practice is to utilize a single portal structure and govern landing page visibility dynamically using Persona assignments and role privileges.",
    150: "Web Portal is the default out-of-the-box standard portal rule type provided by Pega Platform for knowledge workers and case processors.",
    152: "Pega enables dashboard customization tailored to distinct Personas so that managers, caseworkers, and executives see only the KPIs and widgets relevant to their daily responsibilities.",
    153: "User dashboards are initially Private to the creator. To share a personalized dashboard across a team, the user must publish it as Shared and designate the target Access Group.",
    162: "Placing design system assets, UI theming, and company-wide design tokens in the Enterprise/CoE layer ensures uniform styling across all division and departmental applications with centralized updates.",
    164: "While Agile Workbench is an integrated canvas tool for logging real-time user stories and bugs directly inside App Studio, Agile Studio is a full-featured project management system that provides multi-team capacity planning, release tracking, and sprint backlogs.",
    165: "When a new Case Type is created in App Studio, Pega Platform automatically adds a corresponding Feature to the Application Inventory to track user stories and development progress against that case type.",
    172: "The Rule-Admin-Product (RAP) rule defines the entire manifest of rulesets, data instances, and schema updates that Deployment Manager exports and packages through the CI/CD pipeline.",
    173: "Continuous deployment pipelines include automated rollback capabilities that revert pre-existing restore points if test suites fail during deployment, guaranteeing high availability.",
    193: "Pega Constellation includes the X-Ray developer tool, which overlays visual cues, layout containers, and property metadata directly on top of the live user interface for rapid UI debugging."
}

# Apply fixes to the original questions
for q in questions:
    qid = q['id']
    if qid == 93:
        q['title'] = "Data Transform Authoring Environments"
        q['scenario'] = "A team member asserts that Data Transforms can only ever be created and configured in Dev Studio."
        q['question'] = "Which statement accurately evaluates this assertion?"
        q['options'] = [
            "The assertion is correct; Dev Studio is the only workspace that supports Data Transforms.",
            "The assertion is incorrect; Data Transforms can be configured in App Studio via Run Data Transform automation steps and the Data Initialization page.",
            "The assertion is incorrect; Data Transforms can only be created in Admin Studio.",
            "The assertion is incorrect; Data Transforms have been deprecated in modern Pega Platform versions."
        ]
        q['correct_idx'] = 1
        q['correct_answer'] = q['options'][1]
        q['explanation'] = "Data Transforms can be configured in App Studio using the Run Data Transform automation step or through the Data Initialization settings on a Case Type, as well as in Dev Studio."

    if qid in FIXES_ZERO:
        q['correct_idx'] = FIXES_ZERO[qid]
        q['correct_answer'] = q['options'][q['correct_idx']]
    if qid in ENRICH_EXPLANATIONS:
        q['explanation'] = ENRICH_EXPLANATIONS[qid]

# Filter out questions > 212 if any exist
questions = [q for q in questions if q['id'] <= 212]

# Add new 28 questions
all_questions = questions + new_questions

# Re-verify and sync correct_answer
for q in all_questions:
    assert 0 <= q['correct_idx'] < len(q['options']), f"Invalid index in {q['id']}"
    q['correct_answer'] = q['options'][q['correct_idx']]

# Distribute by category
cat_groups = defaultdict(list)
for q in all_questions:
    cat_groups[q.get('category', 'General')].append(q)

sets = {1: [], 2: [], 3: [], 4: []}
set_idx = 1
for cat, qs in sorted(cat_groups.items(), key=lambda x: -len(x[1])):
    for q in qs:
        sets[set_idx].append(q)
        q['exam_set'] = set_idx
        set_idx = (set_idx % 4) + 1

# Sort questions in all_questions by ID
all_questions.sort(key=lambda x: x['id'])

print(f"Total questions ready: {len(all_questions)}")
print(f"Set 1: {len(sets[1])}")
print(f"Set 2: {len(sets[2])}")
print(f"Set 3: {len(sets[3])}")
print(f"Set 4: {len(sets[4])}")

# Save to pega_questions.json
with open('pega_questions.json', 'w', encoding='utf-8') as f:
    json.dump(all_questions, f, indent=2, ensure_ascii=False)
print("Updated pega_questions.json successfully.")

# Save to data.js
js_content = f"// Generated Pega Practice Exam Bank - 240 Questions across 4 Sets\nconst PEGA_QUESTIONS = {json.dumps(all_questions, indent=2, ensure_ascii=False)};\n"
with open('data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Updated data.js successfully.")
