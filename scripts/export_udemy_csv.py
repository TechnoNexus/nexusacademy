import csv
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load the 240 questions
with open('pega_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# Output directory
output_dir = 'udemy_exports'
os.makedirs(output_dir, exist_ok=True)

# Exact 17 headers required by Udemy Practice Test CSV bulk uploader
UDEMY_HEADERS = [
    "Question",
    "Question Type",
    "Answer Option 1",
    "Explanation 1",
    "Answer Option 2",
    "Explanation 2",
    "Answer Option 3",
    "Explanation 3",
    "Answer Option 4",
    "Explanation 4",
    "Answer Option 5",
    "Explanation 5",
    "Answer Option 6",
    "Explanation 6",
    "Correct Answers",
    "Overall Explanation",
    "Domain"
]

def format_question_row(q):
    # If scenario exists, prepend to question text for context
    if q.get('scenario') and q['scenario'].strip():
        full_q_text = f"Scenario: {q['scenario'].strip()}\n\nQuestion: {q['question'].strip()}"
    else:
        full_q_text = q['question'].strip()

    opts = q['options']
    c_idx = q['correct_idx']
    
    # Udemy expects 1-based index for correct answers: "1", "2", "3", or "4"
    correct_answer_str = str(c_idx + 1)
    
    row = [
        full_q_text,
        "multiple-choice",
        opts[0] if len(opts) > 0 else "",
        "", # Explanation 1
        opts[1] if len(opts) > 1 else "",
        "", # Explanation 2
        opts[2] if len(opts) > 2 else "",
        "", # Explanation 3
        opts[3] if len(opts) > 3 else "",
        "", # Explanation 4
        opts[4] if len(opts) > 4 else "",
        "", # Explanation 5
        opts[5] if len(opts) > 5 else "",
        "", # Explanation 6
        correct_answer_str,
        q.get('explanation', '').strip(),
        q.get('category', 'General')
    ]
    return row

def export_set(filename, question_list):
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(UDEMY_HEADERS)
        for q in question_list:
            writer.writerow(format_question_row(q))
    print(f"Exported {len(question_list)} questions to {filepath}")

# Export 4 separate sets of 60 questions
for s_num in range(1, 5):
    set_qs = [q for q in questions if q.get('exam_set') == s_num]
    export_set(f"udemy_practice_exam_set_{s_num}.csv", set_qs)

# Export all 240 questions in one file
export_set("udemy_practice_exam_all_240.csv", questions)

print("Udemy CSV export complete!")
