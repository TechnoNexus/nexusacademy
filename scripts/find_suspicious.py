import json
import re

with open('pega_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print("Checking all 208 questions for alignment between chosen answer and explanation...")

suspicious = []
for q in questions:
    chosen = q['correct_answer'].lower()
    exp = q['explanation'].lower()
    opts = [o.lower() for o in q['options']]
    
    # If the chosen answer words don't appear in the explanation, or if another option has more key words:
    # let's calculate word overlap
    chosen_words = set(re.findall(r'[a-zA-Z0-9_\-]+', chosen)) - {'the', 'a', 'an', 'in', 'on', 'of', 'to', 'is', 'it', 'for', 'that', 'this', 'and', 'or', 'be', 'by', 'as', 'are', 'not'}
    
    overlap = sum(1 for w in chosen_words if w in exp)
    
    # Check other options
    for idx, opt in enumerate(opts):
        if idx == q['correct_idx']:
            continue
        opt_words = set(re.findall(r'[a-zA-Z0-9_\-]+', opt)) - {'the', 'a', 'an', 'in', 'on', 'of', 'to', 'is', 'it', 'for', 'that', 'this', 'and', 'or', 'be', 'by', 'as', 'are', 'not'}
        other_overlap = sum(1 for w in opt_words if w in exp)
        if other_overlap > overlap + 2:
            suspicious.append((q['id'], q['title'], q['correct_idx']+1, idx+1, q['options'], q['explanation']))

print(f"Suspicious questions count: {len(suspicious)}")
for s in suspicious:
    print(f"\n[{s[0]}] {s[1]}: Current chosen Option {s[2]}, but Option {s[3]} has higher overlap")
    print(f"  Options: {s[4]}")
    print(f"  Exp: {s[5]}")
