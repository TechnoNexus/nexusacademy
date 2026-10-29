import json

with open('pega_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

for q in questions:
    if q['title'] == 'Dashboard Organization':
        print(f"[{q['id']}] {q['title']}")
        print(f"  Q: {q['question']}")
        print(f"  Options: {q['options']}")
        print(f"  Chosen: Option {q['correct_idx']+1}: {q['correct_answer']}")
        print(f"  Exp: {q['explanation']}")
