# Architecture and State: Nexus Academy Platform
> **Course 1: Pega Certified System Architect (CSA / CSSA) Scenario Engine**

## Overview
**Nexus Academy** is an enterprise certification and scenario simulation platform. This application implements the core Nexus Academy architecture, featuring **Course 1 (Pega CSA/CSSA)** with **240 total audited scenario questions** organized into **4 balanced 60-question practice mock exams** (Set 1, Set 2, Set 3, Set 4) plus an "All Practice Bank" mode. The application delivers an interactive practice experience mirroring real enterprise exams, enhanced with a 3-attempt progressive feedback mechanism, authentic exam passing evaluation (65% / 39 correct), randomized exam order, question filtering, full concept explanations, Course Catalog navigation, and PWA offline mobile support.

## Nexus Academy Platform Roadmap
- **Course 1 (Active)**: Pega Certified System Architect (CSA & CSSA) Scenario Simulator
- **Course 2 (Upcoming)**: Pega Senior System Architect (CSSA) Advanced Architecture
- **Course 3 (Upcoming)**: Pega Certified Lead System Architect (LSA) Enterprise Patterns
- **Course 4 (Upcoming)**: Pega Certified Business Architect (PCBA) Essentials

## Workspace Layout
```text
c:\AI\Utilities\pega-practise\
├── INSTRUCTIONS.md          # Master session handover & operating instructions (READ FIRST)
├── README.md                # Usage guide and documentation
├── index.html               # Main SPA HTML with Exam Set Selector & Toolbar
├── styles.css               # Pega Academy Design System stylesheet (Dark/Light)
├── app.js                   # Interactive logic, 3-attempt engine, 4-set partition, Fisher-Yates randomizer, PWA install
├── data.js                  # Standalone dataset of 240 questions (Zero CORS issues)
├── pega_questions.json      # Standard JSON dataset export (240 questions)
├── manifest.json            # PWA Web App Manifest (standalone, theme #001a41, set shortcuts)
├── sw.js                    # PWA Service Worker for offline pre-caching and background revalidation
├── icons/                   # PWA vector SVG & high-res PNG icons (192x192, 512x512, maskable)
├── start.bat                # 1-click batch launcher (runs local server on port 8080)
├── build_final_dataset.py   # Dataset compilation script (fixes, additions, 4-set distribution)
├── create_28_questions.py   # 28 scenario questions definition script
├── verify_final_suite.py    # Automated test suite verifying 240 questions, answers, and 60-question sets
├── udemy_exports/           # Pre-formatted 17-column bulk upload CSVs for Udemy Practice Tests
│   ├── udemy_practice_exam_set_1.csv
│   ├── udemy_practice_exam_set_2.csv
│   ├── udemy_practice_exam_set_3.csv
│   ├── udemy_practice_exam_set_4.csv
│   └── udemy_practice_exam_all_240.csv
├── _docs/                   # Documentation tracking
│   ├── architecture_and_state.md
│   ├── build_log_and_roadmap.md
│   └── distribution_and_publishing_masterplan.md # Global publishing & monetization strategy
└── scripts/                 # Extraction, validation, and export scripts
    └── export_udemy_csv.py  # Generates Udemy bulk uploader CSV files
```

## Architecture

### Tech Stack
- **Frontend Architecture**: Standalone Single-Page Application (SPA) using vanilla HTML5, CSS3, and modern ES6+ JavaScript.
- **Data Layer**: 
  - `data.js`: Complete 240 scenario and practice questions structured with scenarios, questions, options, correct answers, explanations, categorized into 21 Pega architectural topics, and partitioned into 4 balanced 60-question sets (`exam_set: 1 | 2 | 3 | 4`).
  - `pega_questions.json`: Standard JSON data export.
  - `localStorage`: Client-side persistence for user attempts, scores, question completion states, bookmarks (`pega_academy_practice_state_v3`), active set preference (`pega_academy_active_set_v3`), and randomized sequence preservation (`pega_academy_shuffled_order_set_<N>_v3`, `pega_academy_is_shuffled_v3`).
- **Design System**:
  - Pega Academy-inspired theme (Deep Navy `#001a41`, Pega Blue `#005bb7`, Cyan accent `#00a3e0`, Emerald `#10b981`, Amber `#f59e0b`, Coral `#ef4444`).
  - Dark and Light mode support with high-contrast accessibility (WCAG compliant).
  - Responsive mobile and desktop layout.

### 4-Set 60-Question Mock Exam Architecture
- **Set 1 (60 Questions)**: Balanced representation across all 21 Pega syllabus domains.
- **Set 2 (60 Questions)**: Balanced representation across all 21 Pega syllabus domains.
- **Set 3 (60 Questions)**: Balanced representation across all 21 Pega syllabus domains.
- **Set 4 (60 Questions)**: Balanced representation across all 21 Pega syllabus domains.
- **All Questions (240 Questions)**: Full repository access for exhaustive review.
- **Passing Benchmark**: Displays real-time pass/fail evaluation against the standard Pega certification benchmark: **65% (39 / 60 correct answers)**.
- **4-Set Performance Matrix**: Interactive overview grid in the Stats modal showing completion, score, and pass/fail status for each set with 1-click switching.

### Random Exam Order Engine
- **Default State**: Shuffled / Random Exam Order (`isShuffled = true` by default).
- **Algorithm**: In-place Fisher-Yates shuffle scoped to the currently active exam set.
- **Persistence**: Shuffled question sequence is saved in `localStorage` per exam set. Page reloads or browser restarts preserve the exact exam sequence and in-progress position.
- **Reshuffle**: A dedicated `🔄 Reshuffle` button and `R` keyboard shortcut generates a fresh random exam order for the active set.
- **Order Toggle**: Users can toggle between `🔀 Random Order` and `📑 Topic Order` at any time without losing answers or progress.

### Core Interactive Engine (3-Attempt Logic)
1. **Attempt 1**:
   - User selects an option and submits.
   - If Correct -> Marks status `correct` (Solved on Attempt 1), displays celebratory banner and detailed explanation.
   - If Incorrect -> Increments attempts to 1. Shows feedback: "Incorrect. 2 attempts remaining." Highlights invalid option and keeps question interactive.
2. **Attempt 2**:
   - User modifies their choice and submits.
   - If Correct -> Marks status `correct` (Solved on Attempt 2), reveals explanation.
   - If Incorrect -> Increments attempts to 2. Shows feedback: "Incorrect. 1 attempt remaining."
3. **Attempt 3 (Final Attempt)**:
   - User submits their 3rd attempt.
   - If Correct -> Marks status `correct` (Solved on Attempt 3), reveals explanation.
   - If Incorrect -> 3 failed attempts reached! Marks status `revealed`.
     - Automatically highlights the Correct Option in green with checkmark.
     - Displays failed selected options with red cross.
     - Reveals full Pega rationale and explanation.
     - Locks options from further attempts while allowing navigation.

### Key Features
- **Progressive Web App (PWA) & Offline Mobile Installation**: Installable directly on iOS, Android, and Desktop with `manifest.json`, Service Worker caching (`sw.js`), custom vector/PNG icons, and an active "Install App" prompt.
- **240 Complete Scenarios & Knowledge Checks** covering all 21 Pega topics (212 from source PDF + 28 realistic author-created scenarios).
- **4 Selectable 60-Question Mock Exams**: Exactly matches the authentic 60-question Pega CSA/CSSA certification format.
- **Authentic Exam Randomization**: Questions appear in randomized order by default, with one-click reshuffle.
- **Visual Attempt Indicator**: 3 animated dots showing state (`● ● ○`).
- **Interactive Question Navigator (60/240 Grid)**: Real-time status colors for each question in exam order.
- **Search & Filters**: Instant search across scenarios and questions + topic filtering per set.
- **Performance Scorecard & Pass/Fail Status**: Live score, accuracy, first-attempt mastery, and 4-set performance matrix.
- **Keyboard Shortcuts**: `1`-`4` or `A`-`D` to select, `Enter` to submit, `←`/`→` to navigate, `R` to reshuffle, `G` for grid.
- **Local Storage**: All progress is automatically persisted in the browser.
- **Zero-Dependency Offline Access**: Double-click `index.html` to run directly in any browser.
