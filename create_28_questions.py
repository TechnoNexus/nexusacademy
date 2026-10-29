import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# The 28 new scenario questions
new_questions = [
    {
        "id": 213,
        "block_num": 213,
        "header": "Work Routing & Organization",
        "title": "Skill-Based Work Routing",
        "category": "Work Routing & Organization",
        "scenario": "A global insurance company processes auto claims in multiple languages. A high-priority claim arrives from a customer who speaks French and requires an adjuster with a 'Level 3 Senior' competency rating.",
        "question": "Which Pega routing mechanism should the System Architect configure to ensure the assignment is directed to an adjuster with both French language capability and the required skill rating?",
        "options": [
            "Route the assignment to the Manager's personal worklist.",
            "Route to a Work Queue using an skilled work group routing rule that evaluates operator skill ratings.",
            "Use round-robin routing across all active operators in the Claims work group.",
            "Create a separate Stage for each language and skill combination."
        ],
        "correct_idx": 1,
        "correct_answer": "Route to a Work Queue using an skilled work group routing rule that evaluates operator skill ratings.",
        "explanation": "Skilled-based routing allows Pega to search a Work Group for available operators whose Operator records possess the necessary skills (e.g., French language) at or above the designated competency rating threshold."
    },
    {
        "id": 214,
        "block_num": 214,
        "header": "Work Routing & Organization",
        "title": "Worklist vs. Work Queue Routing",
        "category": "Work Routing & Organization",
        "scenario": "A mortgage underwriting application requires that initial loan applications are pooled together so that any qualified underwriter on duty can pick up the next available application to review.",
        "question": "How should the routing for the initial loan review assignment step be configured?",
        "options": [
            "Route directly to the current user's Worklist.",
            "Route to a Work Queue accessible to all members of the Underwriters work group.",
            "Route to the reporting manager using business logic routing.",
            "Configure a Wait step that pauses until an underwriter assigns it to themselves."
        ],
        "correct_idx": 1,
        "correct_answer": "Route to a Work Queue accessible to all members of the Underwriters work group.",
        "explanation": "Work Queues (formerly workbaskets) represent shared repositories of assignments that can be accessed and processed by any operator who belongs to the associated work group, facilitating team-wide workload distribution."
    },
    {
        "id": 215,
        "block_num": 215,
        "header": "Case Life Cycle & Process Design",
        "title": "Service Level Agreement Urgency Calculation",
        "category": "Case Life Cycle & Process Design",
        "scenario": "An assignment has an initial urgency of 10. The SLA rule configured on the assignment specifies: Goal of 8 hours (adds 15 urgency), Deadline of 24 hours (adds 25 urgency), and Passed Deadline of 12 hours (adds 20 urgency, repeating twice).",
        "question": "If the assignment remains unresolved after 36 hours (past the first Passed Deadline interval), what is the calculated urgency of the assignment?",
        "options": [
            "50",
            "70",
            "90",
            "100"
        ],
        "correct_idx": 1,
        "correct_answer": "70",
        "explanation": "Initial urgency is 10. Reaching the Goal adds 15 (total 25). Reaching the Deadline adds 25 (total 50). Exceeding the first Passed Deadline adds 20 (total 70). Urgency is cumulative up to a maximum cap of 100."
    },
    {
        "id": 216,
        "block_num": 216,
        "header": "Case Life Cycle & Process Design",
        "title": "Service Level Agreement Scope",
        "category": "Case Life Cycle & Process Design",
        "scenario": "A customer service organization has a strict regulatory requirement that an entire complaint resolution process must be completed within 5 business days from the moment the case enters the 'Investigation' stage, regardless of how many individual tasks or sub-processes occur within that stage.",
        "question": "At which level should the Service Level Agreement (SLA) rule be attached?",
        "options": [
            "Directly on each individual Assignment step within the stage.",
            "On the Investigation Stage itself.",
            "On the primary Process inside the stage.",
            "On the Operator ID of the complaint investigator."
        ],
        "correct_idx": 1,
        "correct_answer": "On the Investigation Stage itself.",
        "explanation": "Attaching an SLA at the Stage level governs the total elapsed duration of the entire stage from entry to completion, regardless of the individual assignment steps executed within it."
    },
    {
        "id": 217,
        "block_num": 217,
        "header": "Case Relationships & Wait Steps",
        "title": "Case Locking Strategies for Parent and Child Cases",
        "category": "Case Relationships & Wait Steps",
        "scenario": "A customer onboarding case spawns two child cases: 'Credit Check' and 'Identity Verification'. Both child cases are frequently processed simultaneously by different back-office agents while the parent case is open.",
        "question": "Which locking strategy should the Lead System Architect configure on the parent case type to prevent locking conflicts when child cases are processed concurrently?",
        "options": [
            "Default locking (lock the parent case when a child case is opened).",
            "Optimistic locking (allow multiple users to open and update the case, verifying changes on submit).",
            "Disable locking completely on all cases.",
            "Configure a Wait step to lock child cases sequentially."
        ],
        "correct_idx": 1,
        "correct_answer": "Optimistic locking (allow multiple users to open and update the case, verifying changes on submit).",
        "explanation": "Optimistic locking allows multiple users to open and work on a case or its child cases simultaneously without locking the parent record exclusively, checking for concurrent edits only when saving/submitting."
    },
    {
        "id": 218,
        "block_num": 218,
        "header": "Case Relationships & Wait Steps",
        "title": "Pausing Workflow with Wait Step",
        "category": "Case Relationships & Wait Steps",
        "scenario": "An order fulfillment case initiates two parallel child cases: 'Inventory Dispatch' and 'Payment Processing'. The parent case must not proceed to the 'Shipping' stage until both child cases have reached the 'Resolved-Completed' status.",
        "question": "How should this workflow synchronization be implemented in the parent case life cycle?",
        "options": [
            "Add a Wait step configured to wait for all child cases to reach the status of 'Resolved-Completed'.",
            "Create an SLA on the Shipping stage set to 24 hours.",
            "Add a Decision Table at the beginning of the Shipping stage to check the status.",
            "Require the customer to manually submit a verification form."
        ],
        "correct_idx": 0,
        "correct_answer": "Add a Wait step configured to wait for all child cases to reach the status of 'Resolved-Completed'.",
        "explanation": "A Wait step can be configured to pause parent case processing until all child cases of a designated type reach a specified resolution status."
    },
    {
        "id": 219,
        "block_num": 219,
        "header": "Case Life Cycle & Process Design",
        "title": "Reverting Workflow via Change Stage",
        "category": "Case Life Cycle & Process Design",
        "scenario": "During the 'Underwriting' stage of a loan case, the underwriter notices that the applicant provided outdated bank statements. The case must be routed back to the initial 'Collect Documents' primary stage to allow the applicant to upload fresh files.",
        "question": "Which Pega feature should be used to move the case backwards to the 'Collect Documents' stage?",
        "options": [
            "The Change Stage smart shape configured to navigate to the 'Collect Documents' stage.",
            "A Wait step configured with a negative timer.",
            "Deleting the current case and instantiating a new one.",
            "Adding an Alternate Stage named 'Rejection' and restarting the application."
        ],
        "correct_idx": 0,
        "correct_answer": "The Change Stage smart shape configured to navigate to the 'Collect Documents' stage.",
        "explanation": "The Change Stage smart shape allows a process to dynamically transition a case to any preceding or succeeding primary or alternate stage within its life cycle."
    },
    {
        "id": 220,
        "block_num": 220,
        "header": "Data Pages & Integration Caching",
        "title": "Selecting Data Page Scope",
        "category": "Data Pages & Integration Caching",
        "scenario": "An e-commerce application needs to display a catalog of product categories and standard currency conversion rates. This data is read-only, identical for all users across the entire system, and is updated only once per day at midnight.",
        "question": "Which Data Page Scope should the System Architect select to optimize memory utilization and system performance?",
        "options": [
            "Thread scope",
            "Requestor scope",
            "Node scope",
            "Case scope"
        ],
        "correct_idx": 2,
        "correct_answer": "Node scope",
        "explanation": "Node-scoped Data Pages are loaded once per Pega JVM node and shared across all active requestors on that node, maximizing memory efficiency for global, static reference data."
    },
    {
        "id": 221,
        "block_num": 221,
        "header": "Data Pages & Integration Caching",
        "title": "Keyed Data Page Efficiency",
        "category": "Data Pages & Integration Caching",
        "scenario": "A medical records application displays a list of 5,000 healthcare clinics. Users frequently look up individual clinic details by ClinicID on various screens. Loading a separate parameterized data page for each lookup generates thousands of clipboard pages.",
        "question": "Which configuration allows the application to load the clinic list once into memory while still enabling fast single-instance retrieval by ClinicID?",
        "options": [
            "Configure the Data Page as a Keyed Data Page and specify ClinicID as the key.",
            "Change the Data Page structure from List to Page and make it Thread-scoped.",
            "Use an Activity with an Obj-Open method on every screen.",
            "Store all clinic details directly in browser local storage via JavaScript."
        ],
        "correct_idx": 0,
        "correct_answer": "Configure the Data Page as a Keyed Data Page and specify ClinicID as the key.",
        "explanation": "A Keyed Data Page maintains a list in memory and allows individual page lookup using a specified key property without reloading the page from the system of record or creating new clipboard pages."
    },
    {
        "id": 222,
        "block_num": 222,
        "header": "Data Pages & Integration Caching",
        "title": "Handling Data Page Errors Gracefully",
        "category": "Data Pages & Integration Caching",
        "scenario": "A Data Page sources customer credit score data from an external REST API. If the external REST service is temporarily unreachable (HTTP 503), the application must not crash or display raw error messages to the user.",
        "question": "What is the recommended Pega best practice for detecting and handling integration errors in a Data Page?",
        "options": [
            "Use a Response Data Transform to evaluate the standard error property pxDataPageHasErrors and set user-friendly error messages.",
            "Delete the connector rule and write custom Java in a section rule.",
            "Set the Data Page edit mode to Savable.",
            "Configure a When rule on the portal header to hide the screen."
        ],
        "correct_idx": 0,
        "correct_answer": "Use a Response Data Transform to evaluate the standard error property pxDataPageHasErrors and set user-friendly error messages.",
        "explanation": "Response Data Transforms execute immediately after data is fetched from an external source. Checking pxDataPageHasErrors allows developers to catch connectivity failures and apply fallback logic or friendly notifications."
    },
    {
        "id": 223,
        "block_num": 223,
        "header": "Savable Data Pages & Persistence",
        "title": "Updating External Systems with Savable Data Pages",
        "category": "Savable Data Pages & Persistence",
        "scenario": "During an address update microjourney, the user enters a new billing address. Upon case approval, the address must be saved directly to an external Oracle CRM database without writing custom database activities.",
        "question": "Which Pega feature allows developers to configure a save plan with an automated database or REST connector step directly within the case flow?",
        "options": [
            "A Savable Data Page referenced in a Save Data Page step.",
            "A Read-Only Data Page called by an Edit Validate rule.",
            "A Declare Expression configured on the primary stage.",
            "An Obj-Save method placed inside a Decision Table."
        ],
        "correct_idx": 0,
        "correct_answer": "A Savable Data Page referenced in a Save Data Page step.",
        "explanation": "Savable Data Pages define a Save Plan (using Database Save, REST connector, or activity) that can be invoked declaratively using the Save Data Page automation step in a case flow."
    },
    {
        "id": 224,
        "block_num": 224,
        "header": "Decision Management & Business Rules",
        "title": "Evaluating Multi-Condition Rules",
        "category": "Decision Management & Business Rules",
        "scenario": "A credit card application must evaluate an applicant's Credit Score, Annual Income, and Employment Duration against five distinct credit limit tiers. If any condition fails, a specific decline reason code must be returned.",
        "question": "Which decision rule type is best suited for evaluating this tabular matrix of multiple inputs to determine a single outcome?",
        "options": [
            "When rule",
            "Decision Table",
            "Declare Expression",
            "Validate rule"
        ],
        "correct_idx": 1,
        "correct_answer": "Decision Table",
        "explanation": "Decision Tables are ideal for evaluating combinations of multiple conditions arranged in rows and columns to return a discrete result from a matrix of business rules."
    },
    {
        "id": 225,
        "block_num": 225,
        "header": "Decision Management & Business Rules",
        "title": "Decision Tree Hierarchical Branching",
        "category": "Decision Management & Business Rules",
        "scenario": "A diagnostic insurance questionnaire requires if/then/else conditional logic where subsequent questions and branch evaluations depend entirely on answers provided to earlier questions (nested branching logic).",
        "question": "Which rule type is specifically optimized for handling hierarchical, deeply nested if-then-else conditions?",
        "options": [
            "Decision Tree",
            "Decision Table",
            "Data Transform",
            "Edit Validate rule"
        ],
        "correct_idx": 0,
        "correct_answer": "Decision Tree",
        "explanation": "Decision Trees evaluate nested if-then-else logic, where each decision branch can drill down into further sub-conditions, making them superior to Decision Tables for hierarchical logic."
    },
    {
        "id": 226,
        "block_num": 226,
        "header": "Security & Access Control",
        "title": "Masking Sensitive Data with ABAC",
        "category": "Security & Access Control",
        "scenario": "To comply with privacy laws (GDPR/HIPAA), customer service representatives must see only the last four digits of a customer's Social Security Number (e.g., ***-**-1234), while compliance managers must be able to view the full unmasked number.",
        "question": "Which Pega Platform security feature should be implemented to enforce dynamic data masking on specific properties based on user roles?",
        "options": [
            "Attribute-Based Access Control (ABAC) Read Policy with Masking.",
            "Role-Based Access Control (RBAC) Access of Role to Object (ARO) set to 0.",
            "Client-Based Access Control (CBAC) consent form.",
            "Deleting the property from the Caseworker portal section."
        ],
        "correct_idx": 0,
        "correct_answer": "Attribute-Based Access Control (ABAC) Read Policy with Masking.",
        "explanation": "ABAC Read Policies allow developers to specify masking rules (such as showing only the last 4 characters) on sensitive properties based on user and case attributes."
    },
    {
        "id": 227,
        "block_num": 227,
        "header": "Security & Access Control",
        "title": "Access Group Role Aggregation",
        "category": "Security & Access Control",
        "scenario": "A user is assigned to an Access Group that contains two Access Roles: 'ClaimsAuthor' (which grants Read access level 5 and Update level 2 to Work-Claims) and 'ClaimsManager' (which grants Read access level 5 and Update level 5 to Work-Claims).",
        "question": "What is the effective Update access level that the user possesses when working on a Work-Claims case?",
        "options": [
            "Update level 2, because the lowest permission role takes precedence.",
            "Update level 5, because Pega grants the most permissive access level across all roles in the access group.",
            "Update level 0, because the conflict denies permission.",
            "The system throws an authorization error until one role is removed."
        ],
        "correct_idx": 1,
        "correct_answer": "Update level 5, because Pega grants the most permissive access level across all roles in the access group.",
        "explanation": "When an Access Group contains multiple Access Roles that define differing access levels for the same class, Pega grants the highest (most permissive) access level."
    },
    {
        "id": 228,
        "block_num": 228,
        "header": "Data Validation & Integrity",
        "title": "Validate Rule vs. Edit Validate Rule",
        "category": "Data Validation & Integrity",
        "scenario": "A lead system architect needs to implement two validation requirements: (1) Ensure an Email Address conforms to a standard email format regex pattern, and (2) Ensure that a Loan Start Date is chronologically earlier than the Loan End Date.",
        "question": "Which combination of validation rules is most appropriate according to Pega best practices?",
        "options": [
            "Use an Edit Validate rule for (1) format pattern matching, and a Validate rule for (2) cross-property date comparison.",
            "Use an Edit Validate rule for both (1) and (2).",
            "Use a Validate rule for (1) and custom JavaScript for (2).",
            "Use a When rule on the portal harness for both requirements."
        ],
        "correct_idx": 0,
        "correct_answer": "Use an Edit Validate rule for (1) format pattern matching, and a Validate rule for (2) cross-property date comparison.",
        "explanation": "Edit Validate rules test single property values against Java/regex patterns (format validation), whereas Validate rules evaluate business logic and cross-property comparisons (e.g., StartDate < EndDate)."
    },
    {
        "id": 229,
        "block_num": 229,
        "header": "Data Validation & Integrity",
        "title": "Stage-Level Entry Validation",
        "category": "Data Validation & Integrity",
        "scenario": "A claims management case must not enter the 'Settlement' stage unless an adjuster has populated the TotalDamageAmount field and attached an approved inspection report.",
        "question": "Where should the System Architect configure this business validation check?",
        "options": [
            "In the Stage Settings on the Settlement stage under Stage Entry Validation.",
            "In an SLA Passed Deadline escalation action.",
            "In the Data initialization section of pyDefault.",
            "On the logout screen of the portal."
        ],
        "correct_idx": 0,
        "correct_answer": "In the Stage Settings on the Settlement stage under Stage Entry Validation.",
        "explanation": "Stage entry validation rules execute before a case transitions into a new stage, ensuring mandatory criteria and business prerequisites are fulfilled before stage entry."
    },
    {
        "id": 230,
        "block_num": 230,
        "header": "Troubleshooting & Debugging Tools",
        "title": "Asynchronous Processing with Queue Processors",
        "category": "Troubleshooting & Debugging Tools",
        "scenario": "After a mortgage application is approved, a notification packet with multiple PDF attachments must be generated and emailed to the applicant. Because PDF generation is computationally heavy, it should run asynchronously in the background without making the user wait.",
        "question": "Which background processing rule should be used to queue and execute this task asynchronously in Pega Platform?",
        "options": [
            "A Queue Processor rule invoked using the Queue-For-Processing smart shape.",
            "A Job Scheduler configured to run once every hour.",
            "An Activity called synchronously from a flow action post-processing.",
            "A Declare Expression configured on the parent case."
        ],
        "correct_idx": 0,
        "correct_answer": "A Queue Processor rule invoked using the Queue-For-Processing smart shape.",
        "explanation": "Queue Processors replace legacy agents for point-to-point asynchronous message queuing. They execute asynchronously in the background and support delayed processing, multi-threading, and automated retries."
    },
    {
        "id": 231,
        "block_num": 231,
        "header": "Troubleshooting & Debugging Tools",
        "title": "Job Schedulers vs. Queue Processors",
        "category": "Troubleshooting & Debugging Tools",
        "scenario": "Every night at 1:00 AM, the banking application must scan all active accounts, identify accounts with past-due balances exceeding 90 days, and flag them for collection review.",
        "question": "Which background processing mechanism is best suited for scheduled, recurring batch jobs across all records?",
        "options": [
            "Job Scheduler",
            "Queue Processor",
            "Wait Step with a 24-hour timer",
            "SLA Goal action"
        ],
        "correct_idx": 0,
        "correct_answer": "Job Scheduler",
        "explanation": "Job Schedulers are designed for recurring, time-triggered background batch operations (such as running every night at a specific time), whereas Queue Processors process discrete queue items triggered by case events."
    },
    {
        "id": 232,
        "block_num": 232,
        "header": "Troubleshooting & Debugging Tools",
        "title": "Investigating Rule Execution with Tracer",
        "category": "Troubleshooting & Debugging Tools",
        "scenario": "A developer reports that a Decision Table is returning an unexpected value of 'Standard' instead of 'Premium'. The developer needs to inspect the step-by-step execution, property values on the clipboard, and rule resolution path in real time.",
        "question": "Which debugging tool in Dev Studio provides real-time event tracing, break points, and clipboard inspection during rule execution?",
        "options": [
            "Tracer",
            "Clipboard tool",
            "Live UI",
            "PAL (Performance Analyzer)"
        ],
        "correct_idx": 0,
        "correct_answer": "Tracer",
        "explanation": "The Tracer tool captures and displays a chronological log of all internal platform events (activities, decision rules, data transforms, and SQL statements) during execution for deep debugging."
    },
    {
        "id": 233,
        "block_num": 233,
        "header": "Data Modeling & Integration",
        "title": "Simulating Data Sources During Development",
        "category": "Data Pages & Integration Caching",
        "scenario": "The external customer credit bureau web service is still under development by the vendor team and will not be available for four weeks. However, the internal Pega development team must continue building and testing the loan approval flow immediately.",
        "question": "How should the System Architect configure the Data Page to provide realistic test data without modifying application flow logic?",
        "options": [
            "Select the 'Simulate data source' option on the Data Page and configure a sample Data Transform.",
            "Hardcode test customer details directly into the loan application section.",
            "Halt development until the vendor completes the web service.",
            "Write custom Java to mock the HTTP socket connection."
        ],
        "correct_idx": 0,
        "correct_answer": "Select the 'Simulate data source' option on the Data Page and configure a sample Data Transform.",
        "explanation": "Pega Data Pages support simulation, allowing developers to test and build against sample data transforms while the actual external integration service is unavailable."
    },
    {
        "id": 234,
        "block_num": 234,
        "header": "Automated Testing & Quality",
        "title": "Scenario Testing vs. Unit Testing",
        "category": "Automated Testing & Quality",
        "scenario": "A business analyst wants to create an automated test that records interactions on the actual user interface—entering values into form fields, clicking buttons, and asserting expected results across a complete case life cycle.",
        "question": "Which testing feature in App Studio is designed for recording and executing end-to-end UI journey tests?",
        "options": [
            "Scenario Testing",
            "PegaUnit test cases",
            "PAL (Performance Analyzer)",
            "Tracer tool"
        ],
        "correct_idx": 0,
        "correct_answer": "Scenario Testing",
        "explanation": "Scenario Testing allows citizen developers and business analysts to record UI interactions directly in App Studio and play them back as automated end-to-end regression tests."
    },
    {
        "id": 235,
        "block_num": 235,
        "header": "Localization & Multi-Language",
        "title": "Localizing Dropdown and Field Labels",
        "category": "Localization & Multi-Language",
        "scenario": "An enterprise portal must be translated into Spanish. While static labels and headings translate cleanly, the values in a 'Claim Status' drop-down list (such as 'Submitted', 'Under Review', and 'Approved') still appear in English.",
        "question": "Which rule type is used in Pega Platform to provide translated text for drop-down prompts, button labels, and property values?",
        "options": [
            "Field Value rules",
            "Data Transform rules",
            "Edit Validate rules",
            "Paragraph rules"
        ],
        "correct_idx": 0,
        "correct_answer": "Field Value rules",
        "explanation": "Field Value rules are the primary mechanism for localizing short text strings, prompt list options, table headers, and drop-down values into different languages."
    },
    {
        "id": 236,
        "block_num": 236,
        "header": "Class Architecture & Inheritance",
        "title": "Enterprise Class Structure (ECS) Layers",
        "category": "Class Architecture & Inheritance",
        "scenario": "A global financial group builds a base commercial lending application intended to be reused by subsidiaries in both North America and Europe, with each subsidiary applying its own localized compliance rules and branding.",
        "question": "In Pega's Enterprise Class Structure (ECS), which layer should contain the generalized assets shared by all subsidiaries?",
        "options": [
            "The Framework layer",
            "The Implementation layer",
            "The Organization layer",
            "The Operator layer"
        ],
        "correct_idx": 0,
        "correct_answer": "The Framework layer",
        "explanation": "The Framework layer defines generalized application assets, data models, and workflows designed to be extended and specialized by specific subsidiary Implementation layers."
    },
    {
        "id": 237,
        "block_num": 237,
        "header": "Configuration Sets",
        "title": "Dynamic Application Customization via Configuration Sets",
        "category": "Configuration Sets",
        "scenario": "Business managers want to adjust the minimum credit score threshold required for auto-approval (e.g. changing it from 700 to 720) directly in App Studio without requiring a developer to update rules in Dev Studio or deploy a new ruleset version.",
        "question": "Which Pega Platform feature enables business users to safely configure and update application business variables directly from App Studio?",
        "options": [
            "Configuration Sets",
            "Access of Role to Object (ARO)",
            "Tracer breakpoints",
            "Branch Rulesets"
        ],
        "correct_idx": 0,
        "correct_answer": "Configuration Sets",
        "explanation": "Configuration Sets in App Studio allow business administrators to adjust application operational variables and thresholds safely without editing rules or deploying code."
    },
    {
        "id": 238,
        "block_num": 238,
        "header": "Duplicate Case Search & Logic",
        "title": "Duplicate Search Basic vs. Weighted Conditions",
        "category": "Duplicate Case Search & Logic",
        "scenario": "A vehicle registration application uses a Search Duplicate Cases step. Basic condition requires that Vehicle VIN must match exactly. Weighted conditions assign 40 points for Matching Owner SSN and 20 points for Matching Address. The threshold is set to 50 points.",
        "question": "If an incoming case has an exact match for Vehicle VIN and Owner SSN, but has a different Address, what does the system do?",
        "options": [
            "The case is NOT flagged as a duplicate because the total weight (40) is below the threshold of 50.",
            "The case is flagged as a duplicate because the Basic condition matched and the score reached 40.",
            "The case is automatically resolved and deleted.",
            "The system rejects the registration immediately."
        ],
        "correct_idx": 0,
        "correct_answer": "The case is NOT flagged as a duplicate because the total weight (40) is below the threshold of 50.",
        "explanation": "To be flagged as a duplicate, an existing case must satisfy all Basic conditions AND the sum of matching weighted conditions must meet or exceed the threshold (40 < 50, so it is NOT flagged)."
    },
    {
        "id": 239,
        "block_num": 239,
        "header": "User Interface, Portals & Theming",
        "title": "Constellation View-Based Architecture",
        "category": "User Interface, Portals & Theming",
        "scenario": "An enterprise is modernizing their Pega applications by migrating from Theme Cosmos to the Pega Constellation UI architecture. A citizen developer in App Studio adds fields to a case view.",
        "question": "How does the Constellation UI architecture render and deliver these views to the end user's browser?",
        "options": [
            "Constellation separates business logic from presentation using a microservices-based React engine that fetches view metadata and data via DX APIs.",
            "Constellation compiles server-side Java Server Pages (JSPs) directly into static HTML tables.",
            "Constellation requires developers to manually author CSS style sheets for every individual view.",
            "Constellation renders only native desktop software and does not support web browsers."
        ],
        "correct_idx": 0,
        "correct_answer": "Constellation separates business logic from presentation using a microservices-based React engine that fetches view metadata and data via DX APIs.",
        "explanation": "Pega Constellation uses a modern single-page architecture where a client-side React UI engine communicates with Pega Platform purely via RESTful Digital Experience (DX) APIs, delivering responsive performance."
    },
    {
        "id": 240,
        "block_num": 240,
        "header": "Agile Delivery & CI/CD Pipelines",
        "title": "Pipeline Automation with Deployment Manager",
        "category": "Agile Delivery & CI/CD Pipelines",
        "scenario": "A development team packages a new release into a Product Rule (RAP). Before the package is promoted to Production, Deployment Manager must ensure code quality standards are enforced.",
        "question": "Which automated verification step does Deployment Manager execute to prevent low-quality code from advancing to Production?",
        "options": [
            "Enforcing Guardrail Compliance score thresholds and automated PegaUnit test pass rates.",
            "Checking whether developers worked overtime hours in Agile Workbench.",
            "Requiring all operators to log out of the development environment.",
            "Deleting all branch rulesets automatically before testing begins."
        ],
        "correct_idx": 0,
        "correct_answer": "Enforcing Guardrail Compliance score thresholds and automated PegaUnit test pass rates.",
        "explanation": "Deployment Manager automates DevOps quality gates by requiring that Guardrail Compliance scores meet acceptable minimums (e.g. >= 97) and that automated regression/unit test suites pass before promotion."
    }
]

print(f"Defined {len(new_questions)} new scenario questions (IDs 213-240).")
