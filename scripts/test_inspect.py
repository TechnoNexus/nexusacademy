import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('extracted_raw.txt', 'r', encoding='utf-8') as f:
    raw_text = f.read()

# Let's inspect the sections in extracted_raw.txt
# Let's print out the content of section 182, 183, 184, 185
with open('sections_parsed.json', 'r', encoding='utf-8') as f:
    sections = json.load(f)

for i in [0, 1, 2, 3, 9, 10, 92, 93, 182, 183, 184, 185]:
    if i < len(sections):
        print(f"=== SECTION {i}: {sections[i]['header']} ===")
        print(sections[i]['content'][:350])
        print("...")
