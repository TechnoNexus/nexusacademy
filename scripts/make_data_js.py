import json

with open('pega_questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

js_content = f"// Auto-generated Pega Practice Exam Questions ({len(questions)} questions)\nconst PEGA_QUESTIONS = {json.dumps(questions, indent=2, ensure_ascii=False)};\n"

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Generated data.js with {len(questions)} questions!")
