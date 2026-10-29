import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\u200b', ' ').replace('\ufffd', "'")
text = re.sub(r'[●○]\s*', '', text)

# Insert marker before the second question inside Practice Question 1
text = text.replace(
    "A developer is troubleshooting an application. Tracer shows:",
    "Question: Tracer Troubleshooting Sequence\nA developer is troubleshooting an application. Tracer shows:"
)

# Also let's check Aapke web page questions:
# Let's inspect how many blocks we get when splitting by standard headers
pattern = r'(?:^|\n)(?=(?:Scenario\s+\d+:|Rule Search\s*\(Hierarchy\)|Practice Question\s+\d+|Question:\s*Tracer Troubleshooting|Question\s+\d+[\s:⭐][^\n]+|Check\s+\d+:))'
raw_blocks = re.split(pattern, text)

print(f"Total blocks after splitting: {len(raw_blocks)}")
