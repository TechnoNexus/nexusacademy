import json

with open('pega_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Current count: {len(questions)}")

# Add Knowledge Check questions as bonus/complete coverage
extra_questions = [
    {
        "id": len(questions) + 1,
        "block_num": 9991,
        "header": "Knowledge Check: Multi-Step Optional Action",
        "title": "Identifying Multi-Step Optional Action",
        "category": "Case Life Cycle & Process Design",
        "scenario": "A System Architect is reviewing design requirements for optional actions in various business applications.",
        "question": "Select the use case that requires an optional Action with multiple Steps.",
        "options": [
            "A user updates their phone number on the current screen without leaving the assignment.",
            "An operator adds an ad-hoc note to the case history.",
            "A travel booking application allows the customer to modify or cancel in-progress reservations.",
            "A reviewer approves or rejects an expense claim from a single popup modal."
        ],
        "correct_idx": 2,
        "correct_answer": "A travel booking application allows the customer to modify or cancel in-progress reservations.",
        "explanation": "Because modifying or cancelling a flight reservation requires a series of multiple steps (checking existing reservations, date/flight selection, price recalculation, and payment/cancellation confirmation), it requires an Optional Process rather than a single-screen Optional User Action."
    },
    {
        "id": len(questions) + 2,
        "block_num": 9992,
        "header": "Knowledge Check: Core Authoring Studios",
        "title": "Core Authoring Studios in Pega Platform",
        "category": "Studio Architecture & Low-Code",
        "scenario": "Pega Platform provides role-based authoring workspaces called Studios to tailor tools to different team members.",
        "question": "Which three authoring studios are found in Pega Platform?",
        "options": [
            "App Studio, Dev Studio, and Admin Studio",
            "App Studio, Security Studio, and Cloud Studio",
            "Dev Studio, Integration Studio, and UX Studio",
            "Admin Studio, Prediction Studio, and Database Studio"
        ],
        "correct_idx": 0,
        "correct_answer": "App Studio, Dev Studio, and Admin Studio",
        "explanation": "The primary authoring workspaces in Pega Platform are App Studio (low-code citizen and business architects), Dev Studio (system architects and advanced technical rules), and Admin Studio (system administrators). Prediction Studio is specialized for data science and AI models."
    },
    {
        "id": len(questions) + 3,
        "block_num": 9993,
        "header": "Knowledge Check: Parallel Development Benefits",
        "title": "Benefit of Parallel Development with Branches",
        "category": "Parallel Development & Team Collaboration",
        "scenario": "Multiple feature teams are building different components for the same Pega application simultaneously.",
        "question": "Which statement describes a benefit of parallel development with Branches?",
        "options": [
            "It permanently eliminates the need for merging code into the base ruleset.",
            "A team of developers can implement application functionality without impacting the developers of other teams.",
            "It automatically deploys untested code directly to the production environment.",
            "It removes all guardrail requirements from the development workflow."
        ],
        "correct_idx": 1,
        "correct_answer": "A team of developers can implement application functionality without impacting the developers of other teams.",
        "explanation": "Branches provide isolated development containers (Branch Rulesets). This allows independent teams to develop new features or fix bugs simultaneously without stepping on each other's changes or breaking active development."
    },
    {
        "id": len(questions) + 4,
        "block_num": 9994,
        "header": "Knowledge Check: Pre-Merge Requirements",
        "title": "Pre-Merge Requirements for Branches",
        "category": "Parallel Development & Team Collaboration",
        "scenario": "A development team finishes implementing a new feature in their branch ruleset and prepares to merge into the base ruleset.",
        "question": "What step does each team need to take before merging their changes to the main application?",
        "options": [
            "Both teams must delete their developer workspaces immediately.",
            "Only the junior developers need to perform unit tests.",
            "Both teams must resolve conflicts that the system detects between their Branch and the application.",
            "The teams must disable the Security Checklist in Deployment Manager."
        ],
        "correct_idx": 2,
        "correct_answer": "Both teams must resolve conflicts that the system detects between their Branch and the application.",
        "explanation": "Pega enforces strict merge conflict detection. Before any Branch ruleset can be merged into the base application rulesets, developers must review and resolve all overlapping rule conflicts."
    }
]

questions.extend(extra_questions)
print(f"Total questions with bonus knowledge checks: {len(questions)}")

with open('pega_questions.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print("Saved updated pega_questions.json!")
