import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Clean zero-width space and replacement characters
text = text.replace('\u200b', ' ')
text = text.replace('\ufffd', "'")
# Clean bullet characters at line start
text = re.sub(r'[●○]\s*', '', text)

pattern = r'(?:^|\n)(?=(?:Scenario\s+\d+:|Rule Search\s*\(Hierarchy\)|Practice Question\s+\d+|Question\s+\d+[\s:⭐]|Check\s+\d+:))'
raw_blocks = re.split(pattern, text)

print(f"Total raw blocks: {len(raw_blocks)}")

b29 = raw_blocks[29]
print("Cleaned Block 29:")
print(b29)

# Now test matching Question: and Option in Block 29
q_match = re.search(r'Question:\s*(.+?)(?=\n(?:Option\s*\d+:|Options:|[A-D]\.|Correct Answer:|Explanation:))', b29, re.DOTALL | re.I)
print("Q match:", bool(q_match), q_match.group(1).strip() if q_match else None)
