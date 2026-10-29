import json
import re

with open('inferred_answers.json', 'r', encoding='utf-8') as f:
    inferred = json.load(f)

print(f"Total inferred: {len(inferred)}")

flagged = []
for item in inferred:
    opts = item['options']
    chosen_idx = item['chosen_idx']
    exp = item['explanation']
    
    # Check if any other option has stronger keyword match in explanation than chosen
    chosen_opt = opts[chosen_idx] if 0 <= chosen_idx < len(opts) else ""
    
    # Check if explanation mentions "Option X"
    m_opt = re.search(r'Option\s*(\d+)', exp, re.I)
    if m_opt:
        exp_opt_num = int(m_opt.group(1)) - 1
        if exp_opt_num != chosen_idx and 'only option' in exp.lower():
            flagged.append((item['id'], item['title'], f"Explanation says Option {exp_opt_num+1}, but chosen was Option {chosen_idx+1}", exp, opts))
            
    # Check if chosen option is empty or invalid
    if chosen_idx < 0 or chosen_idx >= len(opts):
        flagged.append((item['id'], item['title'], "Invalid index", exp, opts))

print(f"Flagged items count: {len(flagged)}")
for f in flagged:
    print(f"[{f[0]}] {f[1]}: {f[2]}")
    print(f"  Exp: {f[3]}")
    print(f"  Opts: {f[4]}")
