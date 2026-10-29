import re

with open('extracted_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for all places where questions are defined or headers appear
patterns = [
    r'Scenario\s+\d+:[^\n]+',
    r'Practice Question\s+\d+',
    r'Question\s+\d+:[^\n]+',
    r'Question\s+\d+\s+⭐[^\n]+',
    r'Check\s+\d+:[^\n]+'
]

matches = list(re.finditer('|'.join(patterns), text))
print(f"Total question header matches: {len(matches)}")

for i in range(min(15, len(matches))):
    m = matches[i]
    print(f"{i+1}: {m.group(0)}")
