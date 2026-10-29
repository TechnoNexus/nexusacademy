import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\u200b', ' ').replace('\ufffd', "'")
text = re.sub(r'[●○]\s*', '', text)

pattern = r'(?:^|\n)(?=(?:Scenario\s+\d+:|Rule Search\s*\(Hierarchy\)|Practice Question\s+\d+|Question\s+\d+[\s:⭐]|Check\s+\d+:))'
raw_blocks = re.split(pattern, text)

for i in [183, 184, 185, 186]:
    if i < len(raw_blocks):
        print(f"=== BLOCK {i} ===")
        print(repr(raw_blocks[i][:500]))
