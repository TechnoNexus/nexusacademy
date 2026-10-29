# Nexus Academy - Enterprise Certification Simulator
> **Course 1: Pega Certified System Architect (CSA) Scenario Engine**

**Nexus Academy** is an enterprise-grade learning and certification simulation platform. This application hosts **Course 1**, featuring **240 audited scenario questions** organized into **4 balanced 60-question mock exams** with an authentic 3-attempt progressive feedback engine and a 65% certification passing evaluation.

## Nexus Academy Platform Architecture

- **Course 1 (Active)**: *Pega Certified System Architect (CSA)* - 240 high-yield scenarios across 4 balanced 60-question mock exams.
- **Course 2 (Upcoming)**: *Pega Senior System Architect (CSSA) Advanced Architecture*
- **Course 3 (Upcoming)**: *Pega Certified Lead System Architect (LSA) Enterprise Patterns*
- **Course 4 (Upcoming)**: *Pega Certified Business Architect (PCBA) Essentials*

## Course 1 Key Features

- **4 Balanced Practice Exam Sets (60 Questions Each)**:
  - **Set 1 (60 Qs)**, **Set 2 (60 Qs)**, **Set 3 (60 Qs)**, and **Set 4 (60 Qs)**: Each set features a realistic, balanced distribution across all 21 Pega syllabus domains (Modularity, Routing, SLAs, Case Life Cycle, Security, Data Pages, Decisioning, Validation, Background Processing, Constellation UI, CI/CD).
  - **All Practice Bank (240 Qs)**: Option to practice across the entire repository.
  - **Pega Passing Evaluation**: Real-time pass/fail evaluation against the standard **65% passing threshold (39 / 60 correct answers)**.
  - **4-Set Performance Matrix**: An interactive matrix in the Stats modal showing your score, completion, and pass/fail status for each set with 1-click loading.

- **Audited & Verified Answer Integrity**:
  - All questions audited and verified so that marked answers and detailed architectural explanations match 100% (resolved fallback discrepancies such as Question 84 "Validation on a Form").
  - 28 realistic author-created scenarios added covering high-yield topics (SLA calculations, Skill-based routing, ABAC masking, Optimistic vs Default locking, Wait steps, Queue Processors, Job Schedulers, Tracer debugging, etc.).

- **Pega Academy Look & Feel**: Modern, authentic interface designed with Pegasystems corporate blue & cyan aesthetics, clear typography, and responsive cards.

- **Randomized Exam Order (Default)**:
  - Questions are shuffled randomly by default using the Fisher-Yates algorithm within the active set for authentic exam simulation.
  - **`🔄 Reshuffle` button** (or press `R` on keyboard): Generate a fresh random exam order whenever you want to begin a new practice run.
  - **`🔀 Random Order` / `📑 Topic Order` toggle**: Switch between random exam mode and textbook sequential order at any time without losing answers or progress.
  - The random order is persisted in `localStorage` per exam set.

- **3-Attempt Progressive Feedback**:
  - **Attempt 1**: Pick an option and click Submit. If incorrect, get immediate guidance without spoilers ("Incorrect. 2 attempts remaining.").
  - **Attempt 2**: Pick another choice. If incorrect, receive warning feedback ("Incorrect. 1 attempt remaining.").
  - **Attempt 3 (Final)**: If incorrect for the 3rd time, the utility locks further attempts, reveals the official correct answer in vibrant emerald green, flags prior incorrect choices in red, and reveals the comprehensive Pega architectural explanation.
  - **Instant Success**: If solved correctly on any attempt (1, 2, or 3), the utility marks the question as solved, records the attempt number, and presents the concept breakdown.

- **Interactive Question Navigator (60/240 Grid)**:
  - Slide-out drawer with question tiles color-coded by status (Unanswered, In Progress, Correct, Revealed, Bookmarked).
  - Dynamically numbered to match your current exam order with tooltips for scenario names and original IDs.

- **Smart Filters & Search**:
  - Filter by Topic Category or Status within the active exam set.
  - Live instant keyword search across scenarios, rules, and options.

- **Live Scorecard & Topic Mastery**:
  - Tracks total score, accuracy rate, first-try mastery count, progress bar, and topic breakdown.
  - Set-specific performance breakdown and 4-set comparison matrix.

- **Offline & Local Storage Ready**:
  - No database or backend required.
  - All progress, attempts, and bookmarks are automatically saved to your browser's `localStorage`.
  - Works directly by double-clicking `index.html` (zero CORS issues).

## How to Run

### Option 1: Direct File Launch (No Server Needed)
Double-click `index.html` or open it in any modern browser:
```text
file:///c:/AI/Utilities/pega-practise/index.html
```

### Option 2: Using the Included Launcher
Double-click `start.bat` or run:
```powershell
python -m http.server 8080
```
Then open `http://localhost:8080` in your browser.

## Keyboard Shortcuts
- `1` - `4` or `A` - `D`: Select option
- `Enter`: Submit answer
- `←` / `→`: Previous / Next question
- `R`: Reshuffle questions into a fresh random order
- `G`: Toggle Question Grid Navigator
- `Esc`: Close Drawer / Modal
