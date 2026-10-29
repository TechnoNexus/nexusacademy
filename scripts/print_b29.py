import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'(?:^|\n)(?=(?:●\s*)?(?:Scenario\s+\d+:|Rule Search\s*\(Hierarchy\)|Practice Question\s+\d+|Question\s+\d+[\s:⭐]|Check\s+\d+:))'
raw_blocks = re.split(pattern, text)

print("Block 29:")
print(repr(raw_blocks[29]))
