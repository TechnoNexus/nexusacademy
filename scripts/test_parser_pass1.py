import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace unicode replacement character
text = text.replace('\ufffd', "'")

# We can find all blocks
# A block starts at any of:
# (Scenario \d+:|Rule Search \(Hierarchy\)|Practice Question \d+|Question \d+[\s:⭐]|Check \d+:)
pattern = r'(?:^|\n)(?=(?:●\s*)?(?:Scenario\s+\d+:|Rule Search\s*\(Hierarchy\)|Practice Question\s+\d+|Question\s+\d+[\s:⭐]|Check\s+\d+:))'
raw_blocks = re.split(pattern, text)

print(f"Total raw blocks: {len(raw_blocks)}")

def parse_block(b_raw, block_idx):
    # clean page markers inside block and keep track of pages
    pages = [int(p) for p in re.findall(r'---PAGE_(\d+)---', b_raw)]
    b = re.sub(r'---PAGE_\d+---\n?', '', b_raw).strip()
    
    # Check for notes or topic headers embedded before or after
    # e.g., Topic: ... or Google Keep Note: ... or Aapke web page ...
    topic_match = re.search(r'(?:Topic:\s*([^\n]+)|Google Keep Note:\s*([^\n]+))', b)
    topic_str = topic_match.group(1) or topic_match.group(2) if topic_match else None
    
    # Extract header line (first line)
    lines = [l.strip() for l in b.split('\n') if l.strip()]
    if not lines:
        return None
    
    header_line = lines[0]
    header_line = re.sub(r'^[●○\s\*\-]+', '', header_line).strip()
    
    # Determine block type
    title = header_line
    
    # Try finding Scenario:
    scenario = ""
    scen_match = re.search(r'Scenario:\s*(.+?)(?=\n(?:●\s*)?Question:|\n(?:●\s*)?Option|\nOptions:)', b, re.DOTALL | re.I)
    if scen_match:
        scenario = scen_match.group(1).strip()
        scenario = re.sub(r'\s+', ' ', scenario)
    
    # Try finding Question:
    question = ""
    q_match = re.search(r'(?:●\s*)?Question:\s*(.+?)(?=\n(?:●\s*)?Option|\nOptions:|\n[A-D]\.|\nCorrect Answer:|\nExplanation:)', b, re.DOTALL | re.I)
    if q_match:
        question = q_match.group(1).strip()
        question = re.sub(r'\s+', ' ', question)
    elif 'Practice Question' in header_line or 'Question ' in header_line:
        # e.g. Practice Question 1 \n <scenario> \n <question> \n <options>
        # Let's inspect
        pass
    
    # Try finding Explanation / Reason
    explanation = ""
    exp_match = re.search(r'(?:Explanation|Reason|Why|Logic):\s*(.+?)(?=\n(?:●\s*)?(?:Scenario|Topic|Google Keep|Check|Practice Question|Aapke web page)|$)', b, re.DOTALL | re.I)
    if exp_match:
        explanation = exp_match.group(1).strip()
        explanation = re.sub(r'\s+', ' ', explanation)
        
    return {
        'idx': block_idx,
        'header': header_line,
        'scenario': scenario,
        'question': question,
        'explanation': explanation,
        'pages': pages,
        'raw_len': len(b)
    }

parsed_summary = []
for i in range(1, len(raw_blocks)):
    p = parse_block(raw_blocks[i], i)
    if p:
        parsed_summary.append(p)

print(f"Parsed {len(parsed_summary)} blocks.")
print(f"Missing question: {len([p for p in parsed_summary if not p['question']])}")
print(f"Missing explanation: {len([p for p in parsed_summary if not p['explanation']])}")

for p in parsed_summary:
    if not p['question'] or not p['explanation']:
        print(f"Issue in [{p['idx']}] {p['header']} -> Q: {bool(p['question'])}, Exp: {bool(p['explanation'])}")
