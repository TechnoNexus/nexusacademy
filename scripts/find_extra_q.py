import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\u200b', ' ').replace('\ufffd', "'")
text = re.sub(r'[●○]\s*', '', text)

# Let's check other notes in the document that might contain questions:
# For instance, Knowledge Check on page 15, page 18, page 26!
kc_matches = list(re.finditer(r'Aapke web page[^\n]+', text, re.I))
for k in kc_matches:
    print("Found Aapke web page:", k.group(0))

# Also check "What should the developer do"
w_matches = list(re.finditer(r'What should the developer do\?', text, re.I))
print("What should developer do count:", len(w_matches))
