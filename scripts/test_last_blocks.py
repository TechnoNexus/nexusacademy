import re

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

clean_text = re.sub(r'\n---PAGE_\d+---\n', '\n', text)
clean_text = clean_text.replace('\ufffd', "'")

pattern = r'(?:^|\n)(?=(?:●\s*)?(?:Scenario\s+\d+:|Rule Search\s*\(Hierarchy\)|Practice Question\s+\d+|Question\s+\d+[\s:⭐]|Check\s+\d+:))'
raw_blocks = re.split(pattern, clean_text)

print(f"Total blocks: {len(raw_blocks)}")
for i in range(max(1, len(raw_blocks)-8), len(raw_blocks)):
    print(f"=== Block {i} ===")
    print(raw_blocks[i][:300].strip())
