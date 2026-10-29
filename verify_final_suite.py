import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('pega_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print(f"Total questions in JSON: {len(questions)}")
assert len(questions) == 240, "Expected 240 questions"

# Verify each question
set_counts = {1: 0, 2: 0, 3: 0, 4: 0}
for q in questions:
    qid = q['id']
    opts = q['options']
    c_idx = q['correct_idx']
    c_ans = q['correct_answer']
    exp = q['explanation']
    e_set = q['exam_set']
    
    assert len(opts) == 4, f"ID {qid} does not have 4 options"
    assert 0 <= c_idx < 4, f"ID {qid} invalid c_idx: {c_idx}"
    assert c_ans == opts[c_idx], f"ID {qid} answer string mismatch: '{c_ans}' vs '{opts[c_idx]}'"
    assert exp.strip() != "", f"ID {qid} explanation is empty"
    assert e_set in [1, 2, 3, 4], f"ID {qid} invalid exam set: {e_set}"
    set_counts[e_set] += 1

print("Set counts:", set_counts)
assert set_counts == {1: 60, 2: 60, 3: 60, 4: 60}, "Sets are not 60 each!"

# Check specific questions reported or fixed
q84 = next(q for q in questions if q['id'] == 84)
print(f"ID 84 check: '{q84['correct_answer']}' (idx: {q84['correct_idx']}) - Exp: '{q84['explanation'][:60]}...'")
assert q84['correct_idx'] == 1 and q84['correct_answer'] == "Validation on a Form."

q18 = next(q for q in questions if q['id'] == 18)
assert q18['correct_idx'] == 1 and q18['correct_answer'] == "No action is required."

q130 = next(q for q in questions if q['id'] == 130)
assert q130['correct_idx'] == 3 and "Authentication" in q130['correct_answer']

print("All integrity checks passed with flying colors!")
