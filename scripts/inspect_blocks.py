import re

with open('extracted_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect pages 1 to 5
blocks = text.split('Scenario ')
print(f"Total 'Scenario ' splits: {len(blocks)}")
for b in blocks[1:5]:
    print("----- BLOCK -----")
    print(b[:300].strip())
