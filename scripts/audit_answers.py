import json
import re

with open('extracted_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\u200b', ' ').replace('\ufffd', "'")
text = re.sub(r'[●○]\s*', '', text)

text = text.replace(
    "A developer is troubleshooting an application. Tracer shows:",
    "Question: Tracer Troubleshooting Sequence\nA developer is troubleshooting an application. Tracer shows:"
)

pattern = r'(?:^|\n)(?=(?:Scenario\s+\d+:|Rule Search\s*\(Hierarchy\)|Practice Question\s+\d+|Question:\s*Tracer Troubleshooting|Question\s+\d+[\s:⭐]|Check\s+\d+:))'
raw_blocks = re.split(pattern, text)

with open('pega_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# For each question, check how its answer was found
methods = []
for i in range(1, len(raw_blocks)):
    b = raw_blocks[i]
    q = questions[i-1]
    
    m_ans = re.search(r'(?:Correct Answer|Answer|\u2705 Answer|\u2705 Correct answer):\s*([^\n]+)', b, re.I)
    has_explicit = bool(m_ans)
    ans_text = m_ans.group(1).strip() if m_ans else ""
    methods.append({
        'id': q['id'],
        'title': q['title'],
        'has_explicit': has_explicit,
        'explicit_text': ans_text,
        'chosen_idx': q['correct_idx'],
        'chosen_ans': q['correct_answer'],
        'explanation': q['explanation'],
        'options': q['options']
    })

print(f"Total: {len(methods)}")
print(f"Explicit answers: {len([m for m in methods if m['has_explicit']])}")
print(f"Non-explicit answers (inferred): {len([m for m in methods if not m['has_explicit']])}")

# Let's inspect non-explicit answers
with open('inferred_answers.json', 'w', encoding='utf-8') as f:
    json.dump([m for m in methods if not m['has_explicit']], f, indent=2, ensure_ascii=False)
