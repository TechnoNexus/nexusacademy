import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\u200b', ' ').replace('\ufffd', "'")
text = re.sub(r'[●○]\s*', '', text)

# Split by Scenario / Question / Check / Practice Question
pattern = r'(?:^|\n)(?=(?:Scenario\s+\d+:|Rule Search\s*\(Hierarchy\)|Practice Question\s+\d+|Question\s+\d+[\s:⭐]|Check\s+\d+:))'
raw_blocks = re.split(pattern, text)

print(f"Total raw blocks: {len(raw_blocks)}")

def extract_options(b):
    options = []
    # Try Option 1:, Option 2: ...
    opt_matches = list(re.finditer(r'(?:^|\n)\s*Option\s*(\d+):\s*(.+?)(?=\n\s*Option\s*\d+:|\n\s*Correct Answer:|\n\s*Explanation:|\n\s*Feedback|\u2705|\n\s*Answer:|\n\s*Reason:|\n\s*Why:|\n\s*Logic:|$)', b, re.DOTALL | re.I))
    if len(opt_matches) >= 2:
        for om in opt_matches:
            opt_text = re.sub(r'\s+', ' ', om.group(2)).strip()
            options.append(opt_text)
        return options, 'option_num'
        
    # Try A., B., C., D.
    opt_alpha = list(re.finditer(r'(?:^|\n)\s*([A-D])[\.\)]\s*(.+?)(?=\n\s*[A-D][\.\)]|\n\s*Correct Answer:|\n\s*Explanation:|\n\s*Feedback|\u2705|\n\s*Answer:|\n\s*Reason:|\n\s*Why:|\n\s*Logic:|$)', b, re.DOTALL | re.I))
    if len(opt_alpha) >= 2:
        for om in opt_alpha:
            opt_text = re.sub(r'\s+', ' ', om.group(2)).strip()
            options.append(opt_text)
        return options, 'alpha'
        
    # Try Options:\n line1\n line2...
    opt_block = re.search(r'Options:\s*\n(.+?)(?=\n\s*(?:Correct Answer:|Explanation:|Feedback|\u2705|Answer:|Reason:|Why:|$))', b, re.DOTALL | re.I)
    if opt_block:
        lines = [l.strip() for l in opt_block.group(1).split('\n') if l.strip()]
        # filter out lines that might be other text
        if 2 <= len(lines) <= 6:
            return lines, 'lines'

    # Special for Check 1:
    if 'Check 1' in b:
        return ["True", "False"], 'boolean'
    if 'Check 2' in b:
        return ["The Data initialization page", "In pySetFieldDefaults Data Transform", "In an Edit Validate Rule", "In a Wait Step timer"], 'check2'
        
    # Special for Practice Question 1:
    if 'Practice Question 1' in b:
        m = re.search(r'behavior\?\s*\n(.+?)(?=Feedback|Correct Answer:)', b, re.DOTALL | re.I)
        if m:
            lines = [l.strip() for l in m.group(1).split('\n') if l.strip()]
            return lines, 'lines'
            
    # Special for Practice Question 2:
    if 'Practice Question 2' in b:
        m = re.search(r'requirement\?\s*\n(.+?)(?=Feedback|Correct Answer:)', b, re.DOTALL | re.I)
        if m:
            lines = [l.strip() for l in m.group(1).split('\n') if l.strip()]
            return lines, 'lines'
            
    return [], 'none'

def detect_answer(b, options, explanation):
    # 1. Explicit Correct Answer line
    # e.g. Correct Answer: Option 2
    # e.g. Correct Answer: Option 4
    # e.g. ✅ Answer: C
    # e.g. ✅ Correct answer: B, Breakpoint
    # e.g. Answer: False
    m_opt = re.search(r'(?:Correct Answer|Answer|\u2705 Answer|\u2705 Correct answer):\s*(?:Option\s*(\d+)|([A-D])\b|([^\n]+))', b, re.I)
    if m_opt:
        if m_opt.group(1):
            idx = int(m_opt.group(1)) - 1
            if 0 <= idx < len(options):
                return idx, 'explicit_option_num'
        elif m_opt.group(2):
            idx = ord(m_opt.group(2).upper()) - ord('A')
            if 0 <= idx < len(options):
                return idx, 'explicit_alpha'
        elif m_opt.group(3):
            val = m_opt.group(3).strip().lower()
            for idx, opt in enumerate(options):
                if opt.lower() == val or opt.lower().startswith(val) or val.startswith(opt.lower()):
                    return idx, 'explicit_text'
            for idx, opt in enumerate(options):
                if val in opt.lower() or opt.lower() in val:
                    return idx, 'explicit_text_partial'

    # 2. Check if explanation explicitly says: "Option 3 is correct" or "Only Option 3 follows..."
    m_exp_opt = re.search(r'(?:Only\s+)?Option\s*(\d+)\s*(?:is correct|follows|uses|specifies|provides)', explanation, re.I)
    if m_exp_opt:
        idx = int(m_exp_opt.group(1)) - 1
        if 0 <= idx < len(options):
            return idx, 'explanation_option_num'

    # 3. Match options against explanation
    if explanation and options:
        # Give higher weight to matches at the beginning of explanation
        first_sentence = explanation.split('.')[0]
        
        best_score = -1
        best_idx = -1
        for idx, opt in enumerate(options):
            opt_clean = re.sub(r'^(?:The rule in the |A |An |The |Option \d+: )', '', opt, flags=re.I).strip().lower()
            score = 0
            
            # Extract key nouns / phrases
            words = [w for w in re.split(r'[^a-zA-Z0-9_\.]+', opt_clean) if len(w) > 3 and w not in ('because', 'rule', 'type', 'class', 'with', 'from', 'that', 'this')]
            
            # Check if full opt_clean in explanation
            if opt_clean in first_sentence.lower():
                score += 50
            elif opt_clean in explanation.lower():
                score += 30
                
            # Check word matches in first sentence
            for w in words:
                if re.search(r'\b' + re.escape(w) + r'\b', first_sentence.lower()):
                    score += 15
                elif re.search(r'\b' + re.escape(w) + r'\b', explanation.lower()):
                    score += 5
                    
            if score > best_score:
                best_score = score
                best_idx = idx
                
        if best_score >= 10:
            return best_idx, f'heuristic_{best_score}'

    return -1, 'unresolved'

stats = {'total': 0, 'options_found': 0, 'ans_found': 0, 'unresolved': []}
results = []

for i in range(1, len(raw_blocks)):
    b_raw = raw_blocks[i]
    b = re.sub(r'---PAGE_\d+---\n?', '\n', b_raw).strip()
    lines = [l.strip() for l in b.split('\n') if l.strip()]
    if not lines:
        continue
    stats['total'] += 1
    header = lines[0]
    
    # Question
    question = ""
    q_match = re.search(r'Question:\s*(.+?)(?=\n\s*(?:Option\s*\d+:|Options:|[A-D]\.|Correct Answer:|Feedback / Answer Explanation:|\u2705|Answer:|Explanation:))', b, re.DOTALL | re.I)
    if q_match:
        question = re.sub(r'\s+', ' ', q_match.group(1)).strip()
    else:
        if 'Practice Question' in header or 'Question ' in header:
            # find question
            for line in lines[1:]:
                if re.match(r'^(?:[A-D]\.|Option\s*\d+:|Options:|Correct Answer:|\u2705|Answer:|Feedback|Explanation:|Why:|Reason:)', line, re.I):
                    break
                question += " " + line
            question = re.sub(r'\s+', ' ', question).strip()
        elif 'Check ' in header:
            m_chk = re.match(r'Check\s+\d+:\s*\"?([^\"]+)\"?', header)
            question = m_chk.group(1).strip() if m_chk else header

    # Scenario
    scenario = ""
    scen_match = re.search(r'Scenario:\s*(.+?)(?=\n\s*(?:Question:|[A-D]\.|Option\s*\d+:|Options:))', b, re.DOTALL | re.I)
    if scen_match:
        scenario = re.sub(r'\s+', ' ', scen_match.group(1)).strip()

    # Options
    options, opt_type = extract_options(b)
    if len(options) >= 2:
        stats['options_found'] += 1
        
    # Explanation
    exp_match = re.search(r'(?:Explanation|Feedback / Answer Explanation|Reason|Why|Logic):\s*(.+?)(?=\nTopic:|\nGoogle Keep|\nAapke web page|$)', b, re.DOTALL | re.I)
    explanation = ""
    if exp_match:
        explanation = re.sub(r'\s+', ' ', exp_match.group(1)).strip()
        
    # Answer
    ans_idx, method = detect_answer(b, options, explanation)
    if ans_idx != -1:
        stats['ans_found'] += 1
    else:
        stats['unresolved'].append((i, header, options, explanation[:100]))
        
    results.append({
        'id': i,
        'header': header,
        'scenario': scenario,
        'question': question,
        'options': options,
        'correct_idx': ans_idx,
        'method': method,
        'explanation': explanation
    })

print(f"Total blocks processed: {stats['total']}")
print(f"Options found >= 2: {stats['options_found']}")
print(f"Answers found: {stats['ans_found']}")
print(f"Unresolved: {len(stats['unresolved'])}")

for u in stats['unresolved']:
    print(f"Unresolved [{u[0]}] {u[1]}")
    print(f"  Options ({len(u[2])}): {u[2]}")
    print(f"  Exp: {u[3]}")
