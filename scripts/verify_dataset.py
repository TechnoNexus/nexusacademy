import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('pega_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Total verified questions: {len(questions)}")

# Check category distribution
categories = {}
for q in questions:
    c = q['category']
    categories[c] = categories.get(c, 0) + 1

print("\nCategory Distribution:")
for c, count in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"  {c}: {count}")

# Sample checks
indices_to_check = [0, 1, 2, 3, 4, 10, 28, 50, 75, 100, 125, 150, 182, 183, 184, 200, 207]
print("\nSample Inspection:")
for idx in indices_to_check:
    if idx < len(questions):
        q = questions[idx]
        print(f"\n[{q['id']}] Category: {q['category']} | Title: {q['title']}")
        if q['scenario']:
            print(f"  Scenario: {q['scenario'][:100]}...")
        print(f"  Q: {q['question']}")
        print(f"  Opts ({len(q['options'])}): {q['options']}")
        print(f"  Ans [{q['correct_idx']}]: {q['correct_answer']}")
        print(f"  Exp: {q['explanation'][:120]}...")
