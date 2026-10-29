import json
import re

with open('pega_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Total questions: {len(questions)}")

# Let's inspect which ones used heuristic
heuristic_q = [q for q in questions if q.get('method', '').startswith('heuristic')]
print(f"Heuristic questions count: {len(heuristic_q)}")

for q in heuristic_q[:25]:
    print(f"\n[{q['id']}] {q['title']}")
    print(f"  Q: {q['question']}")
    for i, o in enumerate(q['options']):
        print(f"    {i+1}: {o}")
    print(f"  Chosen: Option {q['correct_idx']+1}: {q['correct_answer']}")
    print(f"  Exp: {q['explanation']}")
