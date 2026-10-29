import pymupdf
import re
import json

pdf_path = r'C:\Users\archi\.gemini\antigravity\brain\316a8afa-cd0d-440a-89b3-2c2fc6df7fb6\.user_uploaded\media_1792568095808_da434c79.pdf'
doc = pymupdf.open(pdf_path)

pages_text = []
for i, page in enumerate(doc):
    t = page.get_text()
    # clean replacement character
    t = t.replace('\ufffd', "'")
    pages_text.append(t)

full_text = '\n'.join(pages_text)

with open('extracted_raw.txt', 'w', encoding='utf-8') as f:
    f.write(full_text)

print(f"Total pages: {len(pages_text)}")
print(f"Total chars: {len(full_text)}")
print('Question: count:', len(re.findall(r'Question:', full_text, re.IGNORECASE)))
print('Scenario count:', len(re.findall(r'Scenario\s*\d*:', full_text, re.IGNORECASE)))
print('Explanation: count:', len(re.findall(r'Explanation:', full_text, re.IGNORECASE)))
print('Correct Answer count:', len(re.findall(r'Correct\s*Answer:', full_text, re.IGNORECASE)))
print('Practice Question count:', len(re.findall(r'Practice Question', full_text, re.IGNORECASE)))
