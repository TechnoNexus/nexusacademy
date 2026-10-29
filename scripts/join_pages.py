import pymupdf
import re
import json

pdf_path = r'C:\Users\archi\.gemini\antigravity\brain\316a8afa-cd0d-440a-89b3-2c2fc6df7fb6\.user_uploaded\media_1792568095808_da434c79.pdf'
doc = pymupdf.open(pdf_path)

all_text = ""
for pno in range(len(doc)):
    page_text = doc[pno].get_text()
    all_text += f"\n---PAGE_{pno+1}---\n" + page_text

with open('full_text_with_pages.txt', 'w', encoding='utf-8') as f:
    f.write(all_text)

print(f"Total pages: {len(doc)}, total characters: {len(all_text)}")
