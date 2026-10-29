import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\u200b', ' ').replace('\ufffd', "'")

# Find all occurrences of Answer:
answers = list(re.finditer(r'(?:Correct Answer|✅ Answer|✅ Correct answer|Answer):\s*([^\n]+)', text, re.I))
print(f"Total answers found: {len(answers)}")
for i, a in enumerate(answers[:30]):
    print(f"{i+1}: {a.group(0).strip()}")
