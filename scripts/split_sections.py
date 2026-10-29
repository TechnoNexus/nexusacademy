import re
import json

with open('extracted_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's clean quotes and bullets
text = text.replace('\ufffd', "'")
text = text.replace('●', '')
text = text.replace('○', '')

# Let's split into chunks based on headers like "Scenario X:" or "Practice Question X" or "Question X"
# Notice that some headers are:
# "Scenario 1: Business Logic Update"
# "Scenario 2: Fixing a Broken UI"
# "Topic: ..."
# "Check 1: ..."
# "Question 1: ..."
# "Practice Question 1"

# Let's find all headers with their start and end positions
header_re = re.compile(
    r'(?:^|\n)(?:'
    r'(?P<scen>Scenario\s+\d+:\s*[^\n]+)|'
    r'(?P<pq>Practice\s+Question\s+\d+)|'
    r'(?P<qstar>Question\s+\d+\s+⭐[^\n]+)|'
    r'(?P<qnum>Question\s+\d+:\s*[^\n]+)|'
    r'(?P<check>Check\s+\d+:\s*[^\n]+)|'
    r'(?P<rule_search>Rule Search\s*\(Hierarchy\))'
    r')',
    re.MULTILINE
)

matches = list(header_re.finditer(text))
print(f"Total sections detected: {len(matches)}")

sections = []
for idx, m in enumerate(matches):
    start = m.start()
    end = matches[idx+1].start() if idx + 1 < len(matches) else len(text)
    header = m.group(0).strip()
    content = text[start:end].strip()
    sections.append({
        'header': header,
        'content': content
    })

print(f"Sample sections:")
for s in sections[:10]:
    print(f"Header: {s['header']}")

with open('sections_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(sections, f, indent=2, ensure_ascii=False)
