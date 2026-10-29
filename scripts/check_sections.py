import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('sections_parsed.json', 'r', encoding='utf-8') as f:
    sections = json.load(f)

print(f"Total sections: {len(sections)}")

anomalies = []
valid_count = 0

for i, sec in enumerate(sections):
    content = sec['content']
    header = sec['header']
    
    # Check if this has question
    has_q = bool(re.search(r'Question:', content, re.I) or 'Practice Question' in header or 'Check ' in header)
    has_exp = bool(re.search(r'Explanation:|Reason:|Why:', content, re.I))
    has_opt = bool(re.search(r'Option\s*\d+:|Options:|A\.\s+|A\)\s+', content, re.I))
    
    if not (has_q and has_opt):
        anomalies.append((i, header, content[:200].replace('\n', ' ')))
    else:
        valid_count += 1

print(f"Valid standard questions: {valid_count}")
print(f"Anomalies / special sections count: {len(anomalies)}")
for idx, h, c in anomalies:
    print(f"[{idx}] {h} -> {repr(c)}")
