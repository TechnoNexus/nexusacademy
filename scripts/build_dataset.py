import json
import re
import os

with open('extracted_raw.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

# Let's clean up characters:
raw = raw.replace('\ufffd', "'").replace('\u200b', '')

print("Raw length:", len(raw))
