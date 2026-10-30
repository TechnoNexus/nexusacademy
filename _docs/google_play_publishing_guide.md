# Google Play Store Publishing & Launch Playbook
> **App Title**: Nexus Academy: Pega CSA Simulator  
> **Package ID**: `com.technonexus.nexusacademy`  
> **Release Target**: Production Track / Closed Testing  
> **Cost**: $0.00 (Zero external fees beyond standard Google Play Developer account)

---

## 1. Production Release Assets Summary

All required Google Play assets have been compiled and verified:

| Asset Type | File Path | Specifications | Status |
| :--- | :--- | :--- | :--- |
| **Android App Bundle (.aab)** | [`android/app/build/outputs/bundle/release/app-release.aab`](file:///c:/AI/Utilities/pega-practise/android/app/build/outputs/bundle/release/app-release.aab) | 3.41 MB, Signed with Release Keystore | ✅ Ready |
| **Release APK (.apk)** | [`android/app/build/outputs/apk/release/app-release.apk`](file:///c:/AI/Utilities/pega-practise/android/app/build/outputs/apk/release/app-release.apk) | 3.58 MB, Direct device installation | ✅ Ready |
| **App Store Icon** | [`google_play_assets/app_icon_512.png`](file:///c:/AI/Utilities/pega-practise/google_play_assets/app_icon_512.png) | 512 x 512 px, 32-bit PNG with alpha | ✅ Ready |
| **Feature Graphic** | [`google_play_assets/feature_graphic_1024x500.png`](file:///c:/AI/Utilities/pega-practise/google_play_assets/feature_graphic_1024x500.png) | 1024 x 500 px, 24-bit PNG | ✅ Ready |
| **Phone Screenshots** | [`google_play_assets/screenshots/`](file:///c:/AI/Utilities/pega-practise/google_play_assets/screenshots) | 4 High-Res Screens (1080 x 2400 px) | ✅ Ready |
| **Privacy Policy** | [`privacy-policy.html`](file:///c:/AI/Utilities/pega-practise/privacy-policy.html) | Standalone zero-data policy | ✅ Ready |
| **Signing Keystore** | [`android/nexusacademy-release-key.jks`](file:///c:/AI/Utilities/pega-practise/android/nexusacademy-release-key.jks) | 2048-bit RSA, 10,000-day validity | ✅ Secured |

---

## 2. Store Listing Copy & Metadata

### App Title (30 characters max)
```text
Nexus Academy: Pega CSA Prep
```

### Short Description (80 characters max)
```text
Master 240 Pega CSA scenario questions with 3-attempt exam simulation offline.
```

### Full Description (4000 characters max)
```text
Prepare and pass your Pega Certified System Architect (CSA) certification exam with Nexus Academy — the premier enterprise scenario practice engine built by Lead System Architects.

Featuring 240 meticulously audited, scenario-based questions organized into 4 realistic 60-question mock exams, Nexus Academy delivers the authentic testing experience you need to succeed on your first attempt.

WHY CHOOSE NEXUS ACADEMY?

1. AUTHENTIC 3-ATTEMPT PROGRESSIVE ENGINE
Unlike standard memorization quizzes, our 3-attempt simulation mirrors the real Pega learning process:
• Attempt 1 & 2: Receive targeted hints and eliminate distractors without spoiling the correct answer.
• Attempt 3: Locks and reveals the official answer alongside deep architectural mechanics, clipboard page scopes, and rule resolution rules.

2. 4 BALANCED 60-QUESTION MOCK EXAMS
Four complete practice tests strictly aligned with the official Pega CSA certification blueprint:
• 60 Questions in each exam set
• Real-time evaluation against the official 65% passing threshold (39/60 correct)
• 4-Set Performance Matrix with instant pass/fail score tracking

3. 100% AUDITED ARCHITECTURAL RATIONALE
Every single question includes:
• Exact scenario problem stems with realistic enterprise constraints
• Deep technical WHY explaining runtime rule execution, locking mechanisms, and guardrails
• Distractor Rationale detailing why alternative options fail in Pega
• CLSA Exam Pro-Tips for rapid recall

4. EXHAUSTIVE 21-TOPIC SYLLABUS COVERAGE
Comprehensive mastery across all core Pega domains:
• Case Management & Work Routing (Skilled Routing, Work Queues vs. Worklists)
• Service Level Agreements (SLAs, Urgency calculations, Escalations)
• Data Modeling & Integration (Data Pages, Scopes, Savable Data Pages, Simulation)
• Security Architecture (ABAC Read Masking, RBAC, Access Groups)
• User Interface (Constellation DX API, Traditional Cosmos, Theming)
• Background Processing (Queue Processors, Job Schedulers, Tracer Debugging)
• Automated Testing & Quality (Scenario Testing, PegaUnit, Deployment Manager)

5. DESIGNED FOR FOCUSED STUDY
• 100% Offline Capability: Practice anywhere without internet connectivity or mobile data usage.
• Zero Ads & Zero Tracking: No banners, no pop-ups, no invasive analytics.
• Native Haptics: Tactile feedback on answer selection and exam completion.
• Hardware Navigation: Seamless back-button handling and question palette jump drawer.
• Dark & Light Modes: WCAG high-contrast themes for night-time study sessions.

Target Certification:
• Pega Certified System Architect (CSA) 8.8+ / '24

Disclaimer: Nexus Academy is an independent educational prep platform developed by TechnoNexus Inc. and is not affiliated with, sponsored by, or endorsed by Pegasystems Inc. All trademarks belong to their respective owners.
```

---

## 3. Google Play Console Step-by-Step Submission Walkthrough

### Step 1: Create Application
1. Log in to your [Google Play Console](https://play.google.com/console).
2. Click **Create app** (top-right).
3. Fill in:
   - **App name**: `Nexus Academy: Pega CSA Prep`
   - **Default language**: `English (United States) – en-US`
   - **App or game**: `App`
   - **Free or paid**: `Free` (or Paid if you prefer upfront app pricing; the app has built-in license unlocking)
4. Accept Developer Program Policies and US Export Laws, then click **Create app**.

### Step 2: Configure Store Settings & Listing Details
1. In the left navigation menu, go to **Grow** → **Store presence** → **Store settings**:
   - **App category**: `Education`
   - **Tags**: Click `Manage tags` and select `Education`, `Training`, `Productivity`, `Reference`
   - **Store listing contact details**:
     - **Email address**: `support@technonexus.ca`
     - **Website**: `https://technonexus.ca`
   - Click **Save**.
2. Next, go to **Store presence** → **Main store listing**:
   - Paste the **Short description** and **Full description** from Section 2 above.
   - Upload Graphics:
     - **App icon**: Upload [`google_play_assets/app_icon_512.png`](file:///c:/AI/Utilities/pega-practise/google_play_assets/app_icon_512.png).
     - **Feature graphic**: Upload [`google_play_assets/feature_graphic_1024x500.png`](file:///c:/AI/Utilities/pega-practise/google_play_assets/feature_graphic_1024x500.png).
     - **Phone screenshots**: Upload all 4 images from [`google_play_assets/screenshots/`](file:///c:/AI/Utilities/pega-practise/google_play_assets/screenshots) (`01_interactive_exam_engine.png`, `02_architectural_deep_dive.png`, etc.).
   - Click **Save**.

### Step 3: Complete App Content Questionnaires (Policy Compliance)
Under **Policy** → **App content**:

1. **Privacy Policy**:
   - Provide the live URL to `privacy-policy.html` (e.g. `https://technonexus.github.io/nexusacademy/privacy-policy.html`).
2. **Ads**:
   - Select **No, my app does not contain ads**.
3. **App Access**:
   - Select **All functionality is available without special access** (or provide test code `NEXUS2026` for the license key field if prompted).
4. **Content Rating (IARC)**:
   - Category: **Utility, Productivity, Communication, or other** / **Education**.
   - Violence, Sex, Language, Controlled Substances: Select **No** to all questions.
   - User interaction: Select **No** (no chat, no user-to-user content sharing).
   - Physical location: Select **No**.
   - Digital Goods: If free app, select **No**.
   - Result: **Rated for 3+ / Everyone** (Cleanest rating).
5. **Target Audience and Content**:
   - Target age: **18 and over** (Educational/Professional).
   - Appeal to children: **No**.
6. **Data Safety**:
   - Does your app collect or share any of the required user data types? Select **No**.
   - (Nexus Academy stores zero data externally; everything stays strictly on device).
7. **Financial Features**:
   - Select **My app does not provide any financial features**.
8. **Government Apps**:
   - Select **No**.

### Step 4: Create Production Release
1. In the left navigation menu, go to **Release** → **Production** (or **Closed testing** if your developer account requires testing tracks).
2. Click **Create new release**.
3. Under **App bundles**, upload:
   [`android/app/build/outputs/bundle/release/app-release.aab`](file:///c:/AI/Utilities/pega-practise/android/app/build/outputs/bundle/release/app-release.aab)
4. Set **Release name**: `1.0.0 (Initial Release)`
5. Set **Release notes** (en-US):
   ```text
   • Complete Course 1: Pega Certified System Architect (CSA) Practice Exam Simulator.
   • 240 Audited scenario-based questions across 4 full-length 60-question mock exams.
   • Interactive 3-attempt progressive hint engine with deep architectural explanations.
   • Real-time pass/fail evaluation against the official 65% certification benchmark.
   • 100% offline access with native haptics and dark/light mode support.
   ```
6. Click **Next** → **Save** → **Review release** → **Start rollout to Production**!

---

## 4. Keystore Security & Backup
> [!IMPORTANT]
> Keep the keystore [`android/nexusacademy-release-key.jks`](file:///c:/AI/Utilities/pega-practise/android/nexusacademy-release-key.jks) safe! It is required to sign future app updates.
- **Keystore file**: `android/nexusacademy-release-key.jks`
- **Alias**: `nexusacademy`
- **Keystore Password**: `nexusacademy2026`
- **Key Password**: `nexusacademy2026`
- **Validity**: 10,000 days (~27 years)
