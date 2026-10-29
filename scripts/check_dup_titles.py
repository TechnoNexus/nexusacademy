import json
from collections import Counter

with open('pega_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

titles = [q['title'] for q in questions]
counts = Counter(titles)
duplicates = {k: v for k, v in counts.items() if v > 1}
print(f"Duplicate titles count: {len(duplicates)}")
for k, v in duplicates.items():
    matching_ids = [q['id'] for q in questions if q['title'] == k]
    print(f"  '{k}' appears {v} times in IDs: {matching_ids}")
