import pymupdf
import re

pdf_path = r'C:\Users\archi\.gemini\antigravity\brain\316a8afa-cd0d-440a-89b3-2c2fc6df7fb6\.user_uploaded\media_1792568095808_da434c79.pdf'
doc = pymupdf.open(pdf_path)

page_contents = []
for pno in range(len(doc)):
    page_contents.append((pno + 1, doc[pno].get_text()))

print("Page count:", len(page_contents))

# Check how questions are distributed across pages
for pno, text in page_contents[:10]:
    scenarios = re.findall(r'Scenario(?:\s+\d+)?:', text)
    print(f"Page {pno}: {len(scenarios)} scenarios, chars: {len(text)}")
