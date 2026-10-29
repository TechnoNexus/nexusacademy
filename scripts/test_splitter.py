import re
import json

def clean_str(s):
    if not s:
        return ""
    # remove bullets and multiple spaces
    s = s.replace('\ufffd', "'")
    s = re.sub(r'^[●○\s\*\-]+', '', s)
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's remove the PAGE markers, but we can replace with double newlines
clean_text = re.sub(r'\n---PAGE_\d+---\n', '\n', text)
clean_text = clean_text.replace('\ufffd', "'")

# Find all blocks:
# A block starts at any of:
# 1. (Scenario \d+:[^\n]+)
# 2. (Rule Search \(Hierarchy\))
# 3. (Practice Question \d+)
# 4. (Question \d+[\s:⭐][^\n]+)
# 5. (Check \d+:[^\n]+)

pattern = r'(?:^|\n)(?=(?:●\s*)?(?:Scenario\s+\d+:|Rule Search\s*\(Hierarchy\)|Practice Question\s+\d+|Question\s+\d+[\s:⭐]|Check\s+\d+:))'
raw_blocks = re.split(pattern, clean_text)
print(f"Total raw blocks: {len(raw_blocks)}")

# Let's print out the first 5 blocks
for i, b in enumerate(raw_blocks[1:6]):
    print(f"--- Block {i+1} ---")
    print(b[:250].strip())
    print("...")
