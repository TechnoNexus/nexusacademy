import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('full_text_with_pages.txt', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\u200b', ' ').replace('\ufffd', "'")
text = re.sub(r'[●○]\s*', '', text)

# Insert marker before the second question inside Practice Question 1
text = text.replace(
    "A developer is troubleshooting an application. Tracer shows:",
    "Question: Tracer Troubleshooting Sequence\nA developer is troubleshooting an application. Tracer shows:"
)

pattern = r'(?:^|\n)(?=(?:Scenario\s+\d+:|Rule Search\s*\(Hierarchy\)|Practice Question\s+\d+|Question:\s*Tracer Troubleshooting|Question\s+\d+[\s:⭐][^\n]+|Check\s+\d+:))'
raw_blocks = re.split(pattern, text)

# Explicit manual overrides for known edge cases by ID or unique title
MANUAL_OVERRIDES_BY_BLOCK = {
    1: {"title": "Business Logic Update", "correct_idx": 1},
    2: {"title": "Fixing a Broken UI", "correct_idx": 2},
    3: {"title": "Rule vs. Rule Type", "correct_idx": 2},
    4: {"title": "Versioning Choice", "correct_idx": 0},
    5: {"title": "Ruleset Naming Conventions", "correct_idx": 2},
    8: {"title": "The New Record Form", "correct_idx": 0},
    11: {"title": "Rule Search (Hierarchy)", "correct_idx": 1},
    12: {"title": "Parent/Child Inheritance", "correct_idx": 1},
    14: {"title": "Search Order Logic", "correct_idx": 1},
    16: {"title": "The Ultimate Base Class", "correct_idx": 1},
    17: {"title": "Bridging Dev Studio and App Studio", "correct_idx": 1},
    96: {"title": "Superclass Data Transform Naming", "correct_idx": 1},
    99: {"title": "Locating List Data", "correct_idx": 1},
    144: {"title": "Understanding User Intent", "correct_idx": 1},
    151: {"title": "Dashboard Organization", "correct_idx": 1},
    183: {"title": "Practice Question 1 - Skip Stage Tool", "correct_idx": 1},
    184: {"title": "Tracer Troubleshooting Sequence", "correct_idx": 2},
    185: {"title": "Practice Question 2 - In-Memory Property Inspection", "correct_idx": 1},
}

def get_category(title, scenario, question):
    combined = (title + " " + scenario + " " + question).lower()
    if any(k in combined for k in ['locale', 'language pack', 'translation', 'pymessages', 'paragraph']):
        return "Localization & Multi-Language"
    if any(k in combined for k in ['tracer', 'clipboard', 'xray', 'redux devtools', 'breakpoint', 'watch', 'debug']):
        return "Troubleshooting & Debugging Tools"
    if any(k in combined for k in ['unit test', 'test pyramid', 'assertion', 'test coverage', 'rule coverage']):
        return "Automated Testing & Quality"
    if any(k in combined for k in ['ci/cd', 'deployment manager', 'pipeline', 'product rule', 'agile workbench', 'agile studio']):
        return "Agile Delivery & CI/CD Pipelines"
    if any(k in combined for k in ['explore data', 'insight', 'reporting', 'chart', 'simple value', 'show/hide']):
        return "Reporting & Explore Data Insights"
    if any(k in combined for k in ['design token', 'wcag', 'theme', 'constellation', 'traditional ui', 'portal', 'dashboard', 'widget', 'channel', 'iva', 'email bot']):
        return "User Interface, Portals & Theming"
    if any(k in combined for k in ['security', 'aic', 'authentication', 'authorization', 'rbac', 'abac', 'cbac', 'access group', 'access role', 'persona', 'privilege', 'aro', 'access deny', 'mfa', 'operator disablement', 'staging level', 'production level']):
        return "Security & Access Control"
    if any(k in combined for k in ['savable data page', 'save data page', 'save plan', 'transaction handling', 'audit note']):
        return "Savable Data Pages & Persistence"
    if any(k in combined for k in ['data page', 'd_', 'pxresults', 'reload if older', 'do not reload', 'scope = node', 'node-scoped', 'simulated', 'report definition']):
        return "Data Pages & Integration Caching"
    if any(k in combined for k in ['data transform', 'pydefault', 'pysetfielddefaults', 'superclass', '@addcalendar']):
        return "Data Transforms & Defaulting"
    if any(k in combined for k in ['edit validate', 'validate rule', 'validation', 'proposed work status']):
        return "Data Validation & Integrity"
    if any(k in combined for k in ['configuration set', 'configuration setting', 'dss', 'condition builder']):
        return "Configuration Sets"
    if any(k in combined for k in ['child case', 'parent case', 'case dependency', 'wait step', 'reference the data', 'propagate']):
        return "Case Relationships & Wait Steps"
    if any(k in combined for k in ['duplicate', 'weighted condition', 'basic condition', 'threshold']):
        return "Duplicate Case Search & Logic"
    if any(k in combined for k in ['branch', 'branching', 'pulse', 'merge conflicts', 'workspace', '#softwarebug']):
        return "Parallel Development & Team Collaboration"
    if any(k in combined for k in ['worklist', 'work queue', 'work group', 'router', 'authorized manager']):
        return "Work Routing & Organization"
    if any(k in combined for k in ['decision table', 'decision tree', 'when rule', 'evaluate all rows', 'show conflicts', 'show completeness', 'otherwise row', 'authority matrix']):
        return "Decision Management & Business Rules"
    if any(k in combined for k in ['stage', 'process modeler', 'optional user action', 'optional process', 'multi-step form', 'draft mode', 'change stage', 'connector action', 'local action', 'yellow rectangle', 'orange diamond', 'blue rectangle', 'green rectangle']):
        return "Case Life Cycle & Process Design"
    if any(k in combined for k in ['app studio', 'dev studio', 'admin studio', 'prediction studio', 'relevant record', 'low-code', 'omnichannel']):
        return "Studio Architecture & Low-Code"
    if any(k in combined for k in ['inheritance', 'class type', 'pattern parent', 'directed parent', '@baseclass', 'work class', 'data class', 'integration class']):
        return "Class Architecture & Inheritance"
    return "Pega Modularity & Core Concepts"

def extract_options(b, header):
    opt_matches = list(re.finditer(r'(?:^|\n)\s*Option\s*(\d+):\s*(.+?)(?=\n\s*Option\s*\d+:|\n\s*Correct Answer:|\n\s*Explanation:|\n\s*Feedback|\u2705|\n\s*Answer:|\n\s*Reason:|\n\s*Why:|\n\s*Logic:|$)', b, re.DOTALL | re.I))
    if len(opt_matches) >= 2:
        options = []
        for om in opt_matches:
            opt_text = re.sub(r'\s+', ' ', om.group(2)).strip()
            options.append(opt_text)
        return options
        
    opt_alpha = list(re.finditer(r'(?:^|\n)\s*([A-D])[\.\)]\s*(.+?)(?=\n\s*[A-D][\.\)]|\n\s*Correct Answer:|\n\s*Explanation:|\n\s*Feedback|\u2705|\n\s*Answer:|\n\s*Reason:|\n\s*Why:|\n\s*Logic:|$)', b, re.DOTALL | re.I))
    if len(opt_alpha) >= 2:
        options = []
        for om in opt_alpha:
            opt_text = re.sub(r'\s+', ' ', om.group(2)).strip()
            options.append(opt_text)
        return options
        
    opt_block = re.search(r'Options:\s*\n(.+?)(?=\n\s*(?:Correct Answer:|Explanation:|Feedback|\u2705|Answer:|Reason:|Why:|$))', b, re.DOTALL | re.I)
    if opt_block:
        lines = [l.strip() for l in opt_block.group(1).split('\n') if l.strip()]
        if 2 <= len(lines) <= 6:
            return lines

    if 'Check 1' in header:
        return ["True", "False"]
    if 'Check 2' in header:
        return ["The Data initialization page", "In pySetFieldDefaults Data Transform", "In an Edit Validate Rule", "In a Wait Step timer"]
        
    if 'Practice Question 1' in header:
        m = re.search(r'behavior\?\s*\n(.+?)(?=Feedback|Correct Answer:)', b, re.DOTALL | re.I)
        if m:
            return [l.strip() for l in m.group(1).split('\n') if l.strip()]
            
    if 'Practice Question 2' in header:
        m = re.search(r'requirement\?\s*\n(.+?)(?=Feedback|Correct Answer:)', b, re.DOTALL | re.I)
        if m:
            return [l.strip() for l in m.group(1).split('\n') if l.strip()]
            
    return []

parsed_questions = []

for i in range(1, len(raw_blocks)):
    b_raw = raw_blocks[i]
    b = re.sub(r'---PAGE_\d+---\n?', '\n', b_raw).strip()
    lines = [l.strip() for l in b.split('\n') if l.strip()]
    if not lines:
        continue
    header = lines[0]
    
    title = re.sub(r'^(?:Scenario\s+\d+:\s*|Question:\s*|Question\s+\d+[\s:⭐]*|Practice Question\s+\d+[\s:]*|Check\s+\d+:?\s*)', '', header).strip()
    if not title:
        title = header
    title = title.strip('"\'')
    
    scenario = ""
    scen_match = re.search(r'Scenario:\s*(.+?)(?=\n\s*(?:Question:|[A-D]\.|Option\s*\d+:|Options:))', b, re.DOTALL | re.I)
    if scen_match:
        scenario = re.sub(r'\s+', ' ', scen_match.group(1)).strip()
        
    question = ""
    q_match = re.search(r'Question:\s*(.+?)(?=\n\s*(?:Option\s*\d+:|Options:|[A-D]\.|Correct Answer:|Feedback / Answer Explanation:|\u2705|Answer:|Explanation:))', b, re.DOTALL | re.I)
    if q_match:
        question = re.sub(r'\s+', ' ', q_match.group(1)).strip()
    else:
        if 'Practice Question' in header or 'Question' in header:
            q_lines = []
            for line in lines[1:]:
                if re.match(r'^(?:[A-D]\.|Option\s*\d+:|Options:|Correct Answer:|\u2705|Answer:|Feedback|Explanation:|Why:|Reason:)', line, re.I):
                    break
                q_lines.append(line)
            question = re.sub(r'\s+', ' ', ' '.join(q_lines)).strip()
        elif 'Check ' in header:
            m_chk = re.match(r'Check\s+\d+:\s*\"?([^\"]+)\"?', header)
            question = m_chk.group(1).strip() if m_chk else header
            
    options = extract_options(b, header)
    
    exp_match = re.search(r'(?:Explanation|Feedback / Answer Explanation|Reason|Why|Logic):\s*(.+?)(?=\n(?:Topic:|Google Keep|Aapke web page)|$)', b, re.DOTALL | re.I)
    explanation = ""
    if exp_match:
        explanation = re.sub(r'\s+', ' ', exp_match.group(1)).strip()

    correct_idx = -1
    
    # Check block manual overrides
    if i in MANUAL_OVERRIDES_BY_BLOCK:
        override = MANUAL_OVERRIDES_BY_BLOCK[i]
        title = override.get("title", title)
        correct_idx = override["correct_idx"]
    else:
        # Check explicit answer
        m_ans = re.search(r'(?:Correct Answer|Answer|\u2705 Answer|\u2705 Correct answer):\s*(?:Option\s*(\d+)|([A-D])\b|([^\n]+))', b, re.I)
        if m_ans:
            if m_ans.group(1):
                idx = int(m_ans.group(1)) - 1
                if 0 <= idx < len(options):
                    correct_idx = idx
            elif m_ans.group(2):
                idx = ord(m_ans.group(2).upper()) - ord('A')
                if 0 <= idx < len(options):
                    correct_idx = idx
            elif m_ans.group(3):
                val = m_ans.group(3).strip().lower()
                for idx, opt in enumerate(options):
                    if opt.lower() == val or opt.lower().startswith(val) or val.startswith(opt.lower()):
                        correct_idx = idx
                        break
                if correct_idx == -1:
                    for idx, opt in enumerate(options):
                        if val in opt.lower() or opt.lower() in val:
                            correct_idx = idx
                            break
                            
        # If still not found, check explanation
        if correct_idx == -1 and explanation and options:
            m_exp_opt = re.search(r'(?:Only\s+)?Option\s*(\d+)\s*(?:is correct|follows|uses|specifies|provides)', explanation, re.I)
            if m_exp_opt:
                idx = int(m_exp_opt.group(1)) - 1
                if 0 <= idx < len(options):
                    correct_idx = idx
            else:
                first_sentence = explanation.split('.')[0]
                best_score = -1
                best_idx = -1
                for idx, opt in enumerate(options):
                    opt_clean = re.sub(r'^(?:The rule in the |A |An |The |Option \d+: )', '', opt, flags=re.I).strip().lower()
                    score = 0
                    words = [w for w in re.split(r'[^a-zA-Z0-9_\.]+', opt_clean) if len(w) > 3 and w not in ('because', 'rule', 'type', 'class', 'with', 'from', 'that', 'this')]
                    if opt_clean in first_sentence.lower():
                        score += 50
                    elif opt_clean in explanation.lower():
                        score += 30
                    for w in words:
                        if re.search(r'\b' + re.escape(w) + r'\b', first_sentence.lower()):
                            score += 15
                        elif re.search(r'\b' + re.escape(w) + r'\b', explanation.lower()):
                            score += 5
                    if score > best_score:
                        best_score = score
                        best_idx = idx
                if best_score >= 10:
                    correct_idx = best_idx

    correct_text = options[correct_idx] if 0 <= correct_idx < len(options) else ""
    category = get_category(title, scenario, question)
    
    parsed_questions.append({
        'id': len(parsed_questions) + 1,
        'block_num': i,
        'header': header,
        'title': title,
        'category': category,
        'scenario': scenario,
        'question': question,
        'options': options,
        'correct_idx': correct_idx,
        'correct_answer': correct_text,
        'explanation': explanation
    })

print(f"Verified & saved {len(parsed_questions)} questions to pega_questions.json!")
with open('pega_questions.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_questions, f, indent=2, ensure_ascii=False)
