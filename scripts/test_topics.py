import json
import re

with open('extracted_raw.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

# Let's see how many pages and how topics are headed
pages = raw.split('=== PAGE ')
print(f"Total page sections: {len(pages)}")

# Let's inspect topic headers across the document
topics = re.findall(r'(?:Topic:\s*([^\n]+)|Google Keep Note:\s*([^\n]+)|Practice Question\s*\d+|Question\s*\d+:\s*([^\n]+))', raw)
print(f"Found topics/notes: {len(topics)}")
