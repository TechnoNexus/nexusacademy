# PROJECT INSTRUCTIONS & SESSION HANDOFF GUIDE
> **READ THIS FIRST IN EVERY NEW SESSION**
> This file is the primary entry point for any AI assistant, developer, or collaborator working on this repository.

---

## 1. Executive Summary & Ultimate Mission

- **Repository**: `c:\AI\Utilities\pega-practise`
- **What this project is**: An enterprise-grade, interactive **Pega Practice Exam Engine & Scenario Bank** built for Pega Certified System Architect (CSA) and Senior System Architect (CSSA) aspirants.
- **Current Content Assets**:
  - **240 High-Yield Scenario Questions**: 212 questions extracted from the 84-page official Pega study material + 28 author-created realistic enterprise scenarios.
  - **100% Audited Answer Integrity**: Every single question's marked correct answer and explanation have been audited and verified to match with zero discrepancies.
  - **4 Balanced Practice Exam Sets (60 Questions each)**: Partitioned into Set 1, Set 2, Set 3, Set 4, each evenly representing all 21 Pega syllabus domains.
  - **3-Attempt Interactive Engine**: Progressive feedback mirroring Pega Academy (Attempt 1 & 2 give guidance without revealing answers; Attempt 3 locks and reveals official answer & concept explanation).
  - **Pega Passing Benchmark**: Real-time evaluation against the 65% certification passing score (39 / 60 correct).
- **OUR ULTIMATE GOAL**:
  > **To publish these questions, scenarios, and practice exams everywhere across the internet** — on Udemy, Unacademy, live public web hosts (GitHub Pages, Vercel), digital storefronts (Gumroad), SEO blogs (Medium, Substack), and developer communities (LinkedIn, Reddit, YouTube).

---

## 2. Directory & Asset Blueprint

```text
c:\AI\Utilities\pega-practise\
│
├── INSTRUCTIONS.md              <-- YOU ARE HERE: Master session handoff & operating instructions
├── README.md                    <-- Public-facing overview & usage guide
├── start.bat                    <-- 1-click batch launcher (runs local server on port 8080)
│
├── index.html                   <-- Modern SPA with Exam Set selector, question cards, drawer, & stats
├── styles.css                   <-- Pega Academy design system (Navy #001a41, Blue #005bb7, Cyan #00a3e0)
├── app.js                       <-- Complete interactive engine (3-attempt loop, Fisher-Yates shuffle, stats)
├── data.js                      <-- Zero-CORS standalone dataset (240 questions across 4 sets)
├── pega_questions.json          <-- Standard JSON export of the 240 questions
│
├── build_final_dataset.py       <-- Master dataset compilation script (fixes, additions, 4-set distribution)
├── create_28_questions.py       <-- Script defining the 28 new high-yield scenario questions (IDs 213–240)
├── verify_final_suite.py        <-- Automated test suite verifying 240 questions, answers, and set sizes
│
├── udemy_exports/               <-- Pre-formatted 17-column bulk upload CSVs for Udemy Practice Tests
│   ├── udemy_practice_exam_set_1.csv   (Set 1 - 60 Questions)
│   ├── udemy_practice_exam_set_2.csv   (Set 2 - 60 Questions)
│   ├── udemy_practice_exam_set_3.csv   (Set 3 - 60 Questions)
│   ├── udemy_practice_exam_set_4.csv   (Set 4 - 60 Questions)
│   └── udemy_practice_exam_all_240.csv (All 240 Questions Bank)
│
├── scripts/
│   └── export_udemy_csv.py      <-- Python generator for Udemy Practice Test CSV bulk uploader
│
└── _docs/                       <-- MANDATORY DOCUMENTATION REPOSITORY
    ├── architecture_and_state.md
    ├── build_log_and_roadmap.md
    └── distribution_and_publishing_masterplan.md  <-- Complete playbook for publishing everywhere
```

---

## 3. How to Run & Verify

1. **Test Dataset Integrity**:
   ```powershell
   python verify_final_suite.py
   ```
   *(Must report 240 questions, 60 questions per set, and 0 assertion errors).*

2. **Re-generate Export CSVs** (if questions change):
   ```powershell
   python scripts/export_udemy_csv.py
   ```

3. **Launch the Local Web App**:
   - Option A: Double-click `index.html` (runs offline via `file:///` with zero server needed).
   - Option B: Double-click `start.bat` or run `python -m http.server 8080` and open `http://localhost:8080`.

---

## 4. Multi-Platform Publishing Roadmap

For in-depth execution details, read [`_docs/distribution_and_publishing_masterplan.md`](file:///c:/AI/Utilities/pega-practise/_docs/distribution_and_publishing_masterplan.md).

| Platform | Format | Asset Ready? | Status / Next Action |
| :--- | :--- | :--- | :--- |
| **Udemy** | 4-Set Practice Test Course (60 Qs each) | ✅ Yes (`udemy_exports/*.csv`) | Upload CSVs via Udemy Instructor Dashboard |
| **Web (Live Public)** | GitHub Pages / Vercel / Netlify | ✅ Yes (`index.html`, `app.js`, `data.js`) | Push repo and enable GitHub Pages for instant live URL |
| **PWA Mobile App** | Installable web app for mobile/desktop | 🔄 In Progress | Add `manifest.json` & service worker |
| **Unacademy** | Educator Video + Quiz Course | 📋 Outline Ready | Submit 3-min demo video on Educator App |
| **Gumroad / Payhip** | Downloadable Study Pack (Web + PDF + JSON) | ✅ Assets Ready | Create Gumroad product listing ($15 - $29) |
| **Medium / Substack** | SEO Articles ("Top Pega Scenario Questions") | 📋 Ready for syndication | Post sample questions linking to the course/web tool |
| **LinkedIn / Reddit** | Community posts (`r/pega`, Pega Devs) | 📋 Ready | Share practice tool links with Pega aspirants |

---

## 5. Mandatory Protocols for Future AI Sessions

Whenever you are asked to add features, update questions, or build new distribution pipelines in this project:

1. **Continuous Documentation Protocol**:
   - Always update `_docs/architecture_and_state.md` and `_docs/build_log_and_roadmap.md`.
   - Never leave documentation out of sync with the codebase.
2. **Answer Integrity Rule**:
   - Never change a question's `correct_idx` without ensuring `correct_answer` and `explanation` match 100%.
   - Always run `python verify_final_suite.py` before completing turns involving question data.
3. **Dual-Format Data Synchronization**:
   - Both `pega_questions.json` and `data.js` must be kept strictly synchronized (handled by `build_final_dataset.py`).
4. **Zero-CORS Offline Capability**:
   - Keep the web utility capable of opening directly from `file:///` without requiring external npm packages or build steps.
