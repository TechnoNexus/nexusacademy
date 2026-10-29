import re
import json

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove page markers but track page numbers if needed
# We can clean \ufffd and special bullets
text = text.replace('\ufffd', "'")

# Let's inspect all major section headings
# Let's see how many scenarios exist
scenario_matches = list(re.finditer(r'(?:^|\n)(?:●\s*)?(Scenario\s+\d+:\s*[^\n]+)', text))
print(f"Scenario X: matches: {len(scenario_matches)}")

# Practice questions and others
pq_matches = list(re.finditer(r'(?:^|\n)(?:●\s*)?(Practice\s+Question\s+\d+|Question\s+\d+[\s:⭐][^\n]+|Check\s+\d+:\s*[^\n]+|Rule Search\s*\(Hierarchy\))', text))
print(f"Other question matches: {len(pq_matches)}")
