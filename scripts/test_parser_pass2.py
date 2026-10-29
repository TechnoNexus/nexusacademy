import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\u200b', ' ').replace('\ufffd', "'")
text = re.sub(r'[●○]\s*', '', text)

pattern = r'(?:^|\n)(?=(?:Scenario\s+\d+:|Rule Search\s*\(Hierarchy\)|Practice Question\s+\d+|Question\s+\d+[\s:⭐]|Check\s+\d+:))'
raw_blocks = re.split(pattern, text)

print(f"Total raw blocks: {len(raw_blocks)}")

def parse_full_block(b_raw, block_idx):
    # track pages
    pages = [int(p) for p in re.findall(r'---PAGE_(\d+)---', b_raw)]
    # remove page markers
    b = re.sub(r'---PAGE_\d+---\n?', '\n', b_raw).strip()
    
    # Check for topics or keep notes at start or end
    topic_match = re.search(r'(?:Topic:\s*([^\n]+)|Google Keep Note:\s*([^\n]+))', b)
    topic_found = topic_match.group(1) or topic_match.group(2) if topic_match else None
    
    lines = [l.strip() for l in b.split('\n') if l.strip()]
    if not lines:
        return None
    header = lines[0]
    
    # 1. Scenario
    scenario = ""
    scen_match = re.search(r'Scenario:\s*(.+?)(?=\n(?:Question:|[A-D]\.|Option\s*\d+:|Options:))', b, re.DOTALL | re.I)
    if scen_match:
        scenario = re.sub(r'\s+', ' ', scen_match.group(1)).strip()
        
    # 2. Question
    question = ""
    q_match = re.search(r'Question:\s*(.+?)(?=\n(?:Option\s*\d+:|Options:|[A-D]\.|Correct Answer:|Feedback / Answer Explanation:|\u2705|Answer:|Explanation:))', b, re.DOTALL | re.I)
    if q_match:
        question = re.sub(r'\s+', ' ', q_match.group(1)).strip()
    else:
        # Check if header is Practice Question or Check
        if 'Practice Question' in header or 'Question ' in header:
            # Maybe question is after context or header
            lines_after = lines[1:]
            # find where options start
            q_lines = []
            for line in lines_after:
                if re.match(r'^(?:[A-D]\.|Option\s*\d+:|Options:|Correct Answer:|\u2705|Answer:|Feedback|Explanation:|Why:|Reason:)', line, re.I):
                    break
                q_lines.append(line)
            question = ' '.join(q_lines).strip()
        elif 'Check ' in header:
            # Check 1: "Data Transforms can be configured only in Dev Studio."
            m_check = re.match(r'Check\s+\d+:\s*\"?([^\"]+)\"?', header)
            if m_check:
                question = m_check.group(1).strip()
            else:
                question = header
    
    # 3. Options
    options = []
    # Try format Option 1: ..., Option 2: ...
    opt_matches = list(re.finditer(r'Option\s*(\d+):\s*(.+?)(?=\nOption\s*\d+:|\nCorrect Answer:|\nExplanation:|\nFeedback|\u2705|\nReason:|\nWhy:|\nLogic:|$)', b, re.DOTALL | re.I))
    if opt_matches:
        for om in opt_matches:
            opt_text = re.sub(r'\s+', ' ', om.group(2)).strip()
            options.append(opt_text)
    
    # If not found, try format A. ..., B. ..., C. ...
    if not options:
        opt_alpha = list(re.finditer(r'(?:^|\n)([A-D])\.\s*(.+?)(?=\n[A-D]\.|\nCorrect Answer:|\nExplanation:|\nFeedback|\u2705|\nAnswer:|\nReason:|\nWhy:|\nLogic:|$)', b, re.DOTALL | re.I))
        if opt_alpha:
            for om in opt_alpha:
                opt_text = re.sub(r'\s+', ' ', om.group(2)).strip()
                options.append(opt_text)
                
    # If not found, try format Options:\nLine 1\nLine 2...
    if not options and 'Options:' in b:
        opt_block = re.search(r'Options:\s*(.+?)(?=\n(?:Correct Answer:|Explanation:|Feedback|\u2705|Answer:|Reason:|Why:|$))', b, re.DOTALL | re.I)
        if opt_block:
            opt_lines = [l.strip() for l in opt_block.group(1).split('\n') if l.strip()]
            options = opt_lines
            
    # If not found and it is Practice Question 1:
    if not options and 'Practice Question 1' in header:
        # Page 71
        # Clipboard \n Tracer \n Performance analysis using Tracer \n Application UI designer
        opt_block = re.search(r'behavior\?\s*(.+?)(?=Feedback|Correct Answer:)', b, re.DOTALL | re.I)
        if opt_block:
            options = [l.strip() for l in opt_block.group(1).split('\n') if l.strip()]
            
    if not options and 'Practice Question 2' in header:
        # Page 72
        # Tracer \n Clipboard \n Request ID analysis \n Tracer performance monitoring
        opt_block = re.search(r'requirement\?\s*(.+?)(?=Feedback|Correct Answer:)', b, re.DOTALL | re.I)
        if opt_block:
            options = [l.strip() for l in opt_block.group(1).split('\n') if l.strip()]
            
    if not options and 'Check 1' in header:
        options = ["True", "False"]
        
    if not options and 'Check 2' in header:
        # Check 2: Where should you set a field to have a default value of 0?
        # Answer: The Data initialization page
        options = ["The Data initialization page", "In pySetFieldDefaults Data Transform", "In an Edit Validate Rule", "In a Wait Step timer"]
        
    # 4. Correct Answer & Explanation
    correct_idx = -1
    correct_text = ""
    
    # Try finding explicit answer
    ans_match = re.search(r'(?:Correct Answer|Answer|\u2705 Answer|\u2705 Correct answer):\s*(?:Option\s*(\d+)|([A-D])(?:,\s*([^\n]+))?|([^\n]+))', b, re.I)
    if ans_match:
        opt_num = ans_match.group(1)
        opt_letter = ans_match.group(2)
        ans_raw = ans_match.group(4) or ans_match.group(3) or ""
        if opt_num:
            correct_idx = int(opt_num) - 1
        elif opt_letter:
            correct_idx = ord(opt_letter.upper()) - ord('A')
        elif ans_raw.strip():
            ans_clean = ans_raw.strip()
            # match with options
            for idx, opt in enumerate(options):
                if ans_clean.lower() in opt.lower() or opt.lower() in ans_clean.lower():
                    correct_idx = idx
                    break
    
    # Explanation
    exp_match = re.search(r'(?:Explanation|Feedback / Answer Explanation|Reason|Why|Logic):\s*(.+?)(?=\nTopic:|\nGoogle Keep|\nAapke web page|$)', b, re.DOTALL | re.I)
    explanation = ""
    if exp_match:
        explanation = re.sub(r'\s+', ' ', exp_match.group(1)).strip()
        
    # If correct_idx is still -1, try to deduce from explanation:
    if correct_idx == -1 and explanation and options:
        # Let's see: often explanation starts with the name of the rule or option
        # Or mentions Option 1, Option 2, Option 3...
        opt_ref = re.search(r'Option\s*(\d+)', explanation, re.I)
        if opt_ref and 'best practice' in explanation.lower():
            # e.g. "Only Option 3 follows all best practices"
            pass
        # Check each option to see if it matches explanation
        # Score each option
        scores = []
        for idx, opt in enumerate(options):
            # Check exact match or phrase match
            clean_opt = re.sub(r'^(The rule in the |A |An |The )', '', opt, flags=re.I).strip()
            score = 0
            if clean_opt.lower() in explanation.lower():
                score += len(clean_opt)
            scores.append((score, idx))
        scores.sort(reverse=True)
        if scores and scores[0][0] > 0:
            # We will review these
            correct_idx = scores[0][1]

    if 0 <= correct_idx < len(options):
        correct_text = options[correct_idx]
        
    return {
        'id': block_idx,
        'header': header,
        'scenario': scenario,
        'question': question,
        'options': options,
        'correct_idx': correct_idx,
        'correct_text': correct_text,
        'explanation': explanation,
        'topic': topic_found,
        'pages': pages
    }

parsed_blocks = []
for i in range(1, len(raw_blocks)):
    p = parse_full_block(raw_blocks[i], i)
    if p:
        parsed_blocks.append(p)

print(f"Total parsed: {len(parsed_blocks)}")
missing_opts = [p for p in parsed_blocks if len(p['options']) < 2]
missing_ans = [p for p in parsed_blocks if p['correct_idx'] == -1]
missing_exp = [p for p in parsed_blocks if not p['explanation']]

print(f"Blocks with < 2 options: {len(missing_opts)}")
print(f"Blocks with missing answer: {len(missing_ans)}")
print(f"Blocks with missing explanation: {len(missing_exp)}")

if missing_opts:
    for m in missing_opts:
        print(f"MISSING OPTS [{m['id']}]: {m['header']}")

if missing_ans:
    for m in missing_ans[:10]:
        print(f"MISSING ANS [{m['id']}]: {m['header']} (opts: {len(m['options'])})")
