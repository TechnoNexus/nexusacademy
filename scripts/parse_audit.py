import re
import json

with open('extracted_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect page markers or split patterns
# We can find questions by splitting or matching.
# Let's see all sections in extracted_raw.txt
lines = text.split('\n')
print(f"Total lines: {len(lines)}")

# Let's find lines that start with Scenario, Question, Option, Explanation, Correct Answer, etc.
sample_lines = [l for l in lines if re.match(r'^(Scenario|Question|Option|Options|Explanation|Correct Answer|Check|\u2705|Answer)', l, re.I)]
print(f"Matched lines count: {len(sample_lines)}")
print("Sample matches:")
for l in sample_lines[:30]:
    print(" ", l)
