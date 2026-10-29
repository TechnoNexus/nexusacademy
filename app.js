// Pega Academy Practice Exam - Interactive Engine
// 240 Questions across 4 Balanced Sets of 60 Questions

(function () {
  'use strict';

  // Freemium Paywall Configuration (Course 1)
  const FREE_QUESTIONS_LIMIT = 7;
  const UNLOCK_STORAGE_KEY = 'nexus_csa_unlocked_v1';
  const VALID_LICENSE_KEYS = ['NEXUS2026', 'NEXUS-CSA-PASS', 'TECHNO-NEXUS-1999', 'PASSCERT2026', 'FULLACCESS'];
  let isCourseUnlocked = false;

  // Storage Keys
  const STORAGE_KEY = 'pega_academy_practice_state_v3';
  const THEME_KEY = 'pega_academy_theme';
  const ACTIVE_SET_KEY = 'pega_academy_active_set_v3';
  const SHUFFLE_ENABLED_KEY = 'pega_academy_is_shuffled_v3';
  const PASSING_THRESHOLD_PCT = 65; // Pega certification standard (65%)
  const PASSING_THRESHOLD_SET = 39;  // 39 out of 60 questions

  const ALL_QUESTIONS = (typeof PEGA_QUESTIONS !== 'undefined' && Array.isArray(PEGA_QUESTIONS)) ? PEGA_QUESTIONS : [];
  
  let activeExamSet = '1'; // '1', '2', '3', '4', or 'all'
  let currentSetQuestions = [];
  let isShuffled = true;
  let questions = []; // Ordered list of current set questions
  let userStates = {}; // id -> { attempts: 0, history: [], status: 'unanswered', bookmarked: false, solvedOnAttempt: null }
  let currentFilteredIndex = 0;
  let filteredQuestions = [];
  let selectedOption = -1;
  let activeDrawerTab = 'all';

  // DOM Elements
  const headerScore = document.getElementById('header-score');
  const headerAccuracy = document.getElementById('header-accuracy');
  const headerProgress = document.getElementById('header-progress');
  const pbarCorrect = document.getElementById('pbar-correct');
  const pbarInProgress = document.getElementById('pbar-in-progress');
  const pbarRevealed = document.getElementById('pbar-revealed');
  const gridBtnText = document.getElementById('grid-btn-text');

  const examSetSelect = document.getElementById('exam-set-select');
  const categorySelect = document.getElementById('category-select');
  const statusFilter = document.getElementById('status-filter');
  const searchInput = document.getElementById('search-input');
  const searchClear = document.getElementById('search-clear');
  const btnBookmark = document.getElementById('btn-bookmark');
  const btnResetQ = document.getElementById('btn-reset-q');

  const btnShuffleToggle = document.getElementById('btn-shuffle-toggle');
  const btnReshuffle = document.getElementById('btn-reshuffle');
  const shuffleBtnText = document.getElementById('shuffle-btn-text');

  const qSetBadge = document.getElementById('q-set-badge');
  const qIndexBadge = document.getElementById('q-index-badge');
  const qOrderBadge = document.getElementById('q-order-badge');
  const qCategoryPill = document.getElementById('q-category-pill');
  const qStatusPill = document.getElementById('q-status-pill');
  const dot1 = document.getElementById('dot-1');
  const dot2 = document.getElementById('dot-2');
  const dot3 = document.getElementById('dot-3');
  const attemptsCountText = document.getElementById('attempts-count-text');

  const scenarioTitle = document.getElementById('scenario-title');
  const scenarioBox = document.getElementById('scenario-box');
  const scenarioText = document.getElementById('scenario-text');
  const questionText = document.getElementById('question-text');
  const optionsContainer = document.getElementById('options-container');

  const feedbackBanner = document.getElementById('feedback-banner');
  const feedbackIcon = document.getElementById('feedback-icon');
  const feedbackTitle = document.getElementById('feedback-title');
  const feedbackMessage = document.getElementById('feedback-message');

  const explanationCard = document.getElementById('explanation-card');
  const expCorrectAnswerText = document.getElementById('exp-correct-answer-text');
  const explanationText = document.getElementById('explanation-text');

  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  const btnSubmit = document.getElementById('btn-submit');

  const btnGridToggle = document.getElementById('btn-grid-toggle');
  const questionDrawer = document.getElementById('question-drawer');
  const drawerBackdrop = document.getElementById('drawer-backdrop');
  const drawerClose = document.getElementById('drawer-close');
  const questionsGrid = document.getElementById('questions-grid');
  const drawerFilterCount = document.getElementById('drawer-filter-count');
  const drawerTabs = document.querySelectorAll('.drawer-tabs .tab-btn');

  const btnSummaryToggle = document.getElementById('btn-summary-toggle');
  const modalBackdrop = document.getElementById('modal-backdrop');
  const modalClose = document.getElementById('modal-close');
  const btnCloseModal = document.getElementById('btn-close-modal');
  const btnResetAll = document.getElementById('btn-reset-all');

  const statTotalQ = document.getElementById('stat-total-q');
  const statTotalLbl = document.getElementById('stat-total-lbl');
  const examStatusCard = document.getElementById('exam-status-card');
  const examStatusTag = document.getElementById('exam-status-tag');
  const examStatusTitle = document.getElementById('exam-status-title');
  const examStatusDesc = document.getElementById('exam-status-desc');
  const examStatusBadge = document.getElementById('exam-status-badge');
  const setsMatrixGrid = document.getElementById('sets-matrix-grid');

  const btnThemeToggle = document.getElementById('btn-theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  const toastContainer = document.getElementById('toast-container');

  const btnCoursesToggle = document.getElementById('btn-courses-toggle');
  const brandHome = document.getElementById('brand-home');
  const coursesModalBackdrop = document.getElementById('courses-modal-backdrop');
  const coursesModalClose = document.getElementById('courses-modal-close');
  const btnCloseCoursesModal = document.getElementById('btn-close-courses-modal');
  const btnContinueCourse1 = document.getElementById('btn-continue-course-1');

  // Initialize Application
  function init() {
    loadTheme();
    loadCourseUnlockState();
    loadUserState();
    loadActiveExamSet();
    initOrdering();
    populateCategories();
    applyFilters();
    renderCurrentQuestion();
    renderQuestionGrid();
    updateOverallStats();
    attachEventListeners();
    initPWA();
  }

  // Freemium Paywall & Unlock State Management
  function loadCourseUnlockState() {
    try {
      const saved = localStorage.getItem(UNLOCK_STORAGE_KEY);
      isCourseUnlocked = (saved === 'true');
    } catch (e) {
      isCourseUnlocked = false;
    }
    updateUnlockUI();
  }

  function updateUnlockUI() {
    const btnUnlockHeader = document.getElementById('btn-unlock-header');
    const unlockBtnText = document.getElementById('unlock-btn-text');
    const courseAccessTag = document.getElementById('course-access-tag');

    if (isCourseUnlocked) {
      if (btnUnlockHeader) {
        btnUnlockHeader.classList.add('unlocked');
        if (unlockBtnText) unlockBtnText.textContent = '⭐ Pro Unlocked';
      }
      if (courseAccessTag) {
        courseAccessTag.className = 'meta-tag pro-tag';
        courseAccessTag.textContent = '⭐ Full Access (240 Qs)';
      }
    } else {
      if (btnUnlockHeader) {
        btnUnlockHeader.classList.remove('unlocked');
        if (unlockBtnText) unlockBtnText.textContent = 'Unlock ($19.99)';
      }
      if (courseAccessTag) {
        courseAccessTag.className = 'meta-tag trial-tag';
        courseAccessTag.textContent = '🎁 Free Preview: 7 Questions';
      }
    }
  }

  function unlockCourse(key) {
    const cleanKey = (key || '').trim().toUpperCase();
    if (VALID_LICENSE_KEYS.includes(cleanKey)) {
      isCourseUnlocked = true;
      try {
        localStorage.setItem(UNLOCK_STORAGE_KEY, 'true');
      } catch (e) {}
      updateUnlockUI();
      renderCurrentQuestion();
      renderQuestionGrid();
      closePaywallModal();
      showToast('🎉 Course Unlocked! All 240 questions and 4 mock exams are now accessible.');
      return true;
    } else {
      const hint = document.getElementById('redeem-hint');
      if (hint) {
        hint.textContent = '❌ Invalid code. Please check your order code or access key.';
        hint.style.color = '#ef4444';
      }
      return false;
    }
  }

  function openPaywallModal(customMessage) {
    const paywallModal = document.getElementById('paywall-modal-backdrop');
    if (paywallModal) {
      if (customMessage) {
        const noticeP = paywallModal.querySelector('.paywall-preview-notice p');
        if (noticeP) noticeP.textContent = customMessage;
      }
      paywallModal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }
  }

  function closePaywallModal() {
    const paywallModal = document.getElementById('paywall-modal-backdrop');
    if (paywallModal) {
      paywallModal.style.display = 'none';
      document.body.style.overflow = '';
    }
  }

  // Active Exam Set Management
  function loadActiveExamSet() {
    if (!isCourseUnlocked) {
      activeExamSet = '1';
      if (examSetSelect) examSetSelect.value = '1';
      refreshSetQuestionPool();
      return;
    }

    try {
      const urlParams = new URLSearchParams(window.location.search);
      const setParam = urlParams.get('set');
      if (setParam && ['1', '2', '3', '4', 'all'].includes(setParam)) {
        activeExamSet = setParam;
      } else {
        const savedSet = localStorage.getItem(ACTIVE_SET_KEY);
        if (savedSet && ['1', '2', '3', '4', 'all'].includes(savedSet)) {
          activeExamSet = savedSet;
        } else {
          activeExamSet = '1';
        }
      }
    } catch (e) {
      activeExamSet = '1';
    }

    if (examSetSelect) {
      examSetSelect.value = activeExamSet;
    }

    refreshSetQuestionPool();
  }

  function refreshSetQuestionPool() {
    if (activeExamSet === 'all') {
      currentSetQuestions = [...ALL_QUESTIONS];
    } else {
      const setNum = parseInt(activeExamSet);
      currentSetQuestions = ALL_QUESTIONS.filter(q => q.exam_set === setNum);
    }
  }

  function switchExamSet(newSet) {
    if (!['1', '2', '3', '4', 'all'].includes(newSet)) return;
    if (!isCourseUnlocked && newSet !== '1') {
      if (examSetSelect) examSetSelect.value = '1';
      openPaywallModal("Practice Exam Sets 2, 3, and 4 are included in the Full Course ($19.99 USD). You can practice Questions 1–7 free in Set 1!");
      return;
    }
    activeExamSet = newSet;
    try {
      localStorage.setItem(ACTIVE_SET_KEY, activeExamSet);
    } catch (e) {}

    if (examSetSelect) {
      examSetSelect.value = activeExamSet;
    }

    refreshSetQuestionPool();
    initOrdering();
    populateCategories();
    categorySelect.value = 'all';
    statusFilter.value = 'all';
    searchInput.value = '';
    searchClear.style.display = 'none';

    currentFilteredIndex = 0;
    applyFilters(false);
    renderCurrentQuestion();
    renderQuestionGrid();
    updateOverallStats();

    const setName = activeExamSet === 'all' ? 'All Practice Bank (240 Questions)' : `Practice Exam Set ${activeExamSet} (60 Questions)`;
    showToast(`Switched to ${setName}`);
  }

  // Question Randomization & Ordering Engine
  function getShuffleKey() {
    return `pega_academy_shuffled_order_set_${activeExamSet}_v3`;
  }

  function generateRandomOrderIds() {
    const ids = currentSetQuestions.map(q => q.id);
    for (let i = ids.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [ids[i], ids[j]] = [ids[j], ids[i]];
    }
    return ids;
  }

  function initOrdering() {
    const storedPref = localStorage.getItem(SHUFFLE_ENABLED_KEY);
    isShuffled = storedPref !== null ? (storedPref === 'true') : true;
    applyOrdering(false);
  }

  function applyOrdering(showNotification = false) {
    if (isShuffled) {
      const shuffleKey = getShuffleKey();
      let savedOrder = null;
      try {
        const raw = localStorage.getItem(shuffleKey);
        if (raw) savedOrder = JSON.parse(raw);
      } catch (e) {
        savedOrder = null;
      }

      if (!Array.isArray(savedOrder) || savedOrder.length !== currentSetQuestions.length) {
        savedOrder = generateRandomOrderIds();
        try {
          localStorage.setItem(shuffleKey, JSON.stringify(savedOrder));
        } catch (e) {}
      }

      const qMap = new Map();
      currentSetQuestions.forEach(q => qMap.set(q.id, q));
      questions = savedOrder.map(id => qMap.get(id)).filter(Boolean);

      if (questions.length !== currentSetQuestions.length) {
        questions = [...currentSetQuestions];
      }
    } else {
      questions = [...currentSetQuestions];
    }

    if (btnShuffleToggle && shuffleBtnText) {
      if (isShuffled) {
        btnShuffleToggle.classList.add('active');
        shuffleBtnText.textContent = 'Random Order';
      } else {
        btnShuffleToggle.classList.remove('active');
        shuffleBtnText.textContent = 'Sequential Order';
      }
    }

    if (qOrderBadge) {
      qOrderBadge.textContent = isShuffled ? '🔀 Exam Order' : '📑 Topic Order';
      qOrderBadge.title = isShuffled ? 'Questions randomized for authentic exam simulation' : 'Sequential topic order';
    }

    if (showNotification) {
      showToast(isShuffled ? '🔀 Exam Mode: Questions randomized' : '📑 Sequential Mode: Original topic order');
    }
  }

  function toggleShuffle() {
    const currentQId = filteredQuestions[currentFilteredIndex] ? filteredQuestions[currentFilteredIndex].id : null;
    isShuffled = !isShuffled;
    try {
      localStorage.setItem(SHUFFLE_ENABLED_KEY, String(isShuffled));
    } catch (e) {}

    applyOrdering(true);
    applyFilters(true);

    if (currentQId) {
      const newIdx = filteredQuestions.findIndex(q => q.id === currentQId);
      if (newIdx !== -1) currentFilteredIndex = newIdx;
    }

    renderCurrentQuestion();
    renderQuestionGrid();
  }

  function reshuffleQuestions() {
    const freshOrder = generateRandomOrderIds();
    try {
      localStorage.setItem(getShuffleKey(), JSON.stringify(freshOrder));
      localStorage.setItem(SHUFFLE_ENABLED_KEY, 'true');
    } catch (e) {}

    isShuffled = true;
    applyOrdering(false);
    currentFilteredIndex = 0;
    applyFilters(false);
    renderCurrentQuestion();
    renderQuestionGrid();
    showToast(`🔄 Exam Set ${activeExamSet} re-shuffled into a fresh random order!`);
  }

  // Load / Save user state from localStorage
  function loadUserState() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        userStates = JSON.parse(saved);
      }
    } catch (e) {
      console.warn("Could not load from localStorage", e);
      userStates = {};
    }

    ALL_QUESTIONS.forEach(q => {
      if (!userStates[q.id]) {
        userStates[q.id] = {
          attempts: 0,
          history: [],
          status: 'unanswered',
          bookmarked: false,
          solvedOnAttempt: null
        };
      }
    });
  }

  function saveUserState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(userStates));
    } catch (e) {
      console.warn("Could not save to localStorage", e);
    }
  }

  // Populate categories dropdown dynamically
  function populateCategories() {
    const counts = {};
    currentSetQuestions.forEach(q => {
      counts[q.category] = (counts[q.category] || 0) + 1;
    });

    const setLabel = activeExamSet === 'all' ? 'All Questions' : `Set ${activeExamSet}`;
    categorySelect.innerHTML = `<option value="all">All Topics (${currentSetQuestions.length} Questions in ${setLabel})</option>`;
    
    const sortedCats = Object.keys(counts).sort();
    sortedCats.forEach(cat => {
      const opt = document.createElement('option');
      opt.value = cat;
      opt.textContent = `${cat} (${counts[cat]})`;
      categorySelect.appendChild(opt);
    });
  }

  // Filter questions based on category, status, and search query
  function applyFilters(keepCurrentQuestion = true) {
    const selectedCat = categorySelect.value;
    const selectedStatus = statusFilter.value;
    const searchTerm = searchInput.value.trim().toLowerCase();

    const currentQId = filteredQuestions[currentFilteredIndex] ? filteredQuestions[currentFilteredIndex].id : null;

    filteredQuestions = questions.filter(q => {
      const state = userStates[q.id] || { status: 'unanswered', bookmarked: false };

      if (selectedCat !== 'all' && q.category !== selectedCat) {
        return false;
      }

      if (selectedStatus === 'unanswered' && state.status !== 'unanswered') return false;
      if (selectedStatus === 'in_progress' && state.status !== 'in_progress') return false;
      if (selectedStatus === 'correct' && state.status !== 'correct') return false;
      if (selectedStatus === 'revealed' && state.status !== 'revealed') return false;
      if (selectedStatus === 'bookmarked' && !state.bookmarked) return false;

      if (searchTerm) {
        const textToSearch = [
          q.title,
          q.scenario,
          q.question,
          q.category,
          ...q.options
        ].join(' ').toLowerCase();

        if (!textToSearch.includes(searchTerm)) {
          return false;
        }
      }

      return true;
    });

    if (filteredQuestions.length === 0) {
      currentFilteredIndex = 0;
    } else if (keepCurrentQuestion && currentQId) {
      const idx = filteredQuestions.findIndex(q => q.id === currentQId);
      currentFilteredIndex = idx !== -1 ? idx : 0;
    } else {
      currentFilteredIndex = 0;
    }

    renderCurrentQuestion();
    renderQuestionGrid();
  }

  // Render Current Question
  function renderCurrentQuestion() {
    if (filteredQuestions.length === 0) {
      renderEmptyState();
      return;
    }

    const q = filteredQuestions[currentFilteredIndex];
    const qState = userStates[q.id] || { attempts: 0, history: [], status: 'unanswered', bookmarked: false };
    selectedOption = -1;

    // Badges & Header
    if (qSetBadge) {
      qSetBadge.textContent = q.exam_set ? `Set ${q.exam_set}` : 'General';
    }

    if (!isCourseUnlocked) {
      qIndexBadge.textContent = `Question ${currentFilteredIndex + 1} of ${FREE_QUESTIONS_LIMIT} (Free Preview) [ID #${q.id}]`;
    } else {
      qIndexBadge.textContent = `Question ${currentFilteredIndex + 1} of ${filteredQuestions.length} (ID #${q.id})`;
    }
    qCategoryPill.textContent = q.category;

    if (qOrderBadge) {
      qOrderBadge.textContent = isShuffled ? '🔀 Exam Order' : '📑 Topic Order';
      qOrderBadge.title = isShuffled ? 'Questions randomized for authentic exam simulation' : 'Sequential topic order';
    }

    // Status pill
    qStatusPill.className = `status-pill status-${qState.status}`;
    if (qState.status === 'unanswered') qStatusPill.textContent = 'Unanswered';
    else if (qState.status === 'in_progress') qStatusPill.textContent = `In Progress (${qState.attempts}/3)`;
    else if (qState.status === 'correct') qStatusPill.textContent = `Correct (Attempt ${qState.solvedOnAttempt || 1})`;
    else if (qState.status === 'revealed') qStatusPill.textContent = 'Revealed (3 Failed)';

    // Bookmark button
    if (qState.bookmarked) {
      btnBookmark.classList.add('bookmarked');
      btnBookmark.innerHTML = '<span class="bookmark-star">★</span> Bookmarked';
    } else {
      btnBookmark.classList.remove('bookmarked');
      btnBookmark.innerHTML = '<span class="bookmark-star">☆</span> Bookmark';
    }

    // Attempts Tracker
    renderAttemptsTracker(qState);

    // Scenario title
    scenarioTitle.textContent = q.title ? q.title : `Question #${q.id}`;

    // Scenario box
    if (q.scenario && q.scenario.trim()) {
      scenarioBox.style.display = 'block';
      scenarioText.textContent = q.scenario;
    } else {
      scenarioBox.style.display = 'none';
      scenarioText.textContent = '';
    }

    // Question Prompt
    questionText.textContent = q.question;

    // Options Container
    renderOptions(q, qState);

    // Feedback & Explanation
    renderFeedbackAndExplanation(q, qState);

    // Navigation buttons state
    btnPrev.disabled = (currentFilteredIndex === 0);
    if (!isCourseUnlocked && currentFilteredIndex === FREE_QUESTIONS_LIMIT - 1) {
      btnNext.disabled = false;
      btnNext.innerHTML = `
        <span>Unlock Course ($19.99)</span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path>
        </svg>
      `;
      btnNext.classList.add('btn-unlock-header');
    } else {
      btnNext.disabled = (currentFilteredIndex === filteredQuestions.length - 1);
      btnNext.innerHTML = `
        <span>Next</span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      `;
      btnNext.classList.remove('btn-unlock-header');
    }

    // Submit button state
    const isLocked = (qState.status === 'correct' || qState.status === 'revealed');
    if (isLocked) {
      btnSubmit.disabled = true;
      btnSubmit.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
        </svg>
        Completed
      `;
    } else {
      btnSubmit.disabled = false;
      const attemptNum = qState.attempts + 1;
      btnSubmit.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        Submit (Attempt ${attemptNum}/3)
      `;
    }

    updateActiveGridItem(q.id);
  }

  // Render 3-dots Attempt Tracker
  function renderAttemptsTracker(qState) {
    attemptsCountText.textContent = `${qState.attempts} / 3`;

    [dot1, dot2, dot3].forEach(d => {
      d.className = 'dot';
    });

    for (let i = 0; i < 3; i++) {
      const dot = [dot1, dot2, dot3][i];
      if (i < qState.attempts) {
        if (qState.status === 'correct' && i === qState.attempts - 1) {
          dot.classList.add('used-success');
        } else {
          dot.classList.add('used-fail');
        }
      } else if (i === qState.attempts && qState.status !== 'correct' && qState.status !== 'revealed') {
        dot.classList.add('active-now');
      }
    }
  }

  // Render Options
  function renderOptions(q, qState) {
    optionsContainer.innerHTML = '';
    const letters = ['A', 'B', 'C', 'D', 'E', 'F'];
    const isLocked = (qState.status === 'correct' || qState.status === 'revealed');

    q.options.forEach((optText, idx) => {
      const card = document.createElement('div');
      card.className = 'option-card';
      card.dataset.index = idx;

      const letterBadge = document.createElement('div');
      letterBadge.className = 'option-letter';
      letterBadge.textContent = letters[idx] || (idx + 1);

      const textDiv = document.createElement('div');
      textDiv.className = 'option-text';
      textDiv.textContent = optText;

      card.appendChild(letterBadge);
      card.appendChild(textDiv);

      if (qState.history && qState.history.includes(idx)) {
        if (idx !== q.correct_idx) {
          card.classList.add('failed-choice');
        }
      }

      if (isLocked) {
        card.classList.add('locked');
        if (idx === q.correct_idx) {
          card.classList.add('correct-answer');
        }
      } else {
        card.addEventListener('click', () => {
          if (isLocked) return;
          selectOption(idx);
        });
      }

      optionsContainer.appendChild(card);
    });
  }

  function selectOption(idx) {
    selectedOption = idx;
    const cards = optionsContainer.querySelectorAll('.option-card');
    cards.forEach(card => {
      if (parseInt(card.dataset.index) === idx) {
        card.classList.add('selected');
      } else {
        card.classList.remove('selected');
      }
    });
  }

  // Feedback & Explanation Rendering
  function renderFeedbackAndExplanation(q, qState) {
    if (qState.status === 'unanswered') {
      feedbackBanner.style.display = 'none';
      explanationCard.style.display = 'none';
      return;
    }

    if (qState.status === 'correct') {
      feedbackBanner.style.display = 'flex';
      feedbackBanner.className = 'feedback-banner success';
      feedbackIcon.textContent = '🎉';
      feedbackTitle.textContent = 'Correct Answer!';
      const tryStr = qState.solvedOnAttempt === 1 ? 'your 1st attempt' : `attempt ${qState.solvedOnAttempt}`;
      feedbackMessage.textContent = `Great job! You solved this question on ${tryStr}. Review the concept explanation below.`;

      explanationCard.style.display = 'block';
      expCorrectAnswerText.textContent = q.correct_answer || q.options[q.correct_idx];
      explanationText.textContent = q.explanation;
      return;
    }

    if (qState.status === 'revealed') {
      feedbackBanner.style.display = 'flex';
      feedbackBanner.className = 'feedback-banner failed';
      feedbackIcon.textContent = '⛔';
      feedbackTitle.textContent = '3 Failed Attempts Reached';
      feedbackMessage.textContent = 'You have used all 3 allowed attempts. The official correct answer and concept explanation have been revealed below.';

      explanationCard.style.display = 'block';
      expCorrectAnswerText.textContent = q.correct_answer || q.options[q.correct_idx];
      explanationText.textContent = q.explanation;
      return;
    }

    if (qState.status === 'in_progress') {
      feedbackBanner.style.display = 'flex';
      feedbackBanner.className = 'feedback-banner warning';
      feedbackIcon.textContent = '⚠️';
      feedbackTitle.textContent = 'Incorrect Choice';
      const remaining = 3 - qState.attempts;
      feedbackMessage.textContent = `That is not the correct answer. You have ${remaining} ${remaining === 1 ? 'attempt' : 'attempts'} remaining. Analyze the question and try another option!`;

      explanationCard.style.display = 'none';
    }
  }

  // Submit Answer
  function submitAnswer() {
    if (filteredQuestions.length === 0) return;
    const q = filteredQuestions[currentFilteredIndex];
    const qState = userStates[q.id];

    if (qState.status === 'correct' || qState.status === 'revealed') {
      showToast('This question has already been completed.');
      return;
    }

    if (selectedOption === -1) {
      showToast('Please select an option before submitting!');
      return;
    }

    const isCorrect = (selectedOption === q.correct_idx);

    if (!qState.history.includes(selectedOption)) {
      qState.history.push(selectedOption);
    }
    qState.attempts += 1;

    if (isCorrect) {
      qState.status = 'correct';
      qState.solvedOnAttempt = qState.attempts;
      showToast(`Correct! Solved on Attempt ${qState.attempts}.`);
    } else {
      if (qState.attempts >= 3) {
        qState.status = 'revealed';
        showToast('3 attempts used. Correct answer revealed.');
      } else {
        qState.status = 'in_progress';
        const rem = 3 - qState.attempts;
        showToast(`Incorrect. ${rem} ${rem === 1 ? 'attempt' : 'attempts'} remaining.`);
      }
    }

    saveUserState();
    updateOverallStats();
    renderCurrentQuestion();
    renderQuestionGrid();

    // Freemium prompt: Trigger paywall when question 7 is completed
    if (!isCourseUnlocked && currentFilteredIndex === FREE_QUESTIONS_LIMIT - 1 && (qState.status === 'correct' || qState.status === 'revealed')) {
      setTimeout(() => {
        openPaywallModal("You've completed all 7 Free Preview Scenarios! Upgrade to the Full Course ($19.99 USD) to practice all 4 mock exams and 240 questions.");
      }, 1400);
    }
  }

  // Empty state when filter produces 0 results
  function renderEmptyState() {
    if (qSetBadge) qSetBadge.textContent = 'No Matches';
    qIndexBadge.textContent = `0 of 0`;
    qCategoryPill.textContent = `No matches`;
    qStatusPill.textContent = `Empty`;
    attemptsCountText.textContent = `0 / 3`;
    scenarioTitle.textContent = `No questions found matching your filter criteria.`;
    scenarioBox.style.display = 'none';
    questionText.textContent = `Try clearing your search query or choosing another topic category.`;
    optionsContainer.innerHTML = '';
    feedbackBanner.style.display = 'none';
    explanationCard.style.display = 'none';
    btnPrev.disabled = true;
    btnNext.disabled = true;
    btnSubmit.disabled = true;
  }

  // Question Navigator Grid Rendering
  function renderQuestionGrid() {
    questionsGrid.innerHTML = '';

    const listToRender = questions.filter(q => {
      const s = userStates[q.id] || { status: 'unanswered', bookmarked: false };
      if (activeDrawerTab === 'all') return true;
      if (activeDrawerTab === 'unanswered') return s.status === 'unanswered';
      if (activeDrawerTab === 'correct') return s.status === 'correct';
      if (activeDrawerTab === 'revealed') return s.status === 'revealed';
      if (activeDrawerTab === 'bookmarked') return s.bookmarked;
      return true;
    });

    drawerFilterCount.textContent = `Showing ${listToRender.length} of ${questions.length} in Set`;

    listToRender.forEach((q, idx) => {
      const s = userStates[q.id] || { status: 'unanswered', bookmarked: false };
      const btn = document.createElement('button');
      btn.className = `grid-btn ${s.status}`;
      btn.textContent = idx + 1;
      btn.dataset.id = q.id;

      if (!isCourseUnlocked && idx >= FREE_QUESTIONS_LIMIT) {
        btn.classList.add('locked');
        btn.title = `Q#${idx + 1} (Locked): Unlock Full Course ($19.99 USD)`;
        btn.addEventListener('click', () => {
          openPaywallModal(`Question #${idx + 1} is part of the Full Course. Upgrade for $19.99 USD to access all 240 questions across all 4 mock exams!`);
          closeDrawer();
        });
      } else {
        btn.title = `Q#${idx + 1} (ID #${q.id}): ${q.title} (${s.status})`;
        if (s.bookmarked) {
          btn.classList.add('bookmarked');
        }

        const currentQ = filteredQuestions[currentFilteredIndex];
        if (currentQ && currentQ.id === q.id) {
          btn.classList.add('current');
        }

        btn.addEventListener('click', () => {
          navigateToQuestionById(q.id);
          closeDrawer();
        });
      }

      questionsGrid.appendChild(btn);
    });
  }

  function updateActiveGridItem(qId) {
    const btns = questionsGrid.querySelectorAll('.grid-btn');
    btns.forEach(b => {
      if (parseInt(b.dataset.id) === qId) {
        b.classList.add('current');
      } else {
        b.classList.remove('current');
      }
    });
  }

  function navigateToQuestionById(qId) {
    let idx = filteredQuestions.findIndex(q => q.id === qId);
    if (!isCourseUnlocked && idx >= FREE_QUESTIONS_LIMIT) {
      openPaywallModal(`Question #${idx + 1} is part of the Full Course. Upgrade for $19.99 USD to unlock all 240 questions!`);
      return;
    }

    if (idx === -1) {
      categorySelect.value = 'all';
      statusFilter.value = 'all';
      searchInput.value = '';
      searchClear.style.display = 'none';
      applyFilters(false);
      idx = filteredQuestions.findIndex(q => q.id === qId);
    }
    if (idx !== -1) {
      if (!isCourseUnlocked && idx >= FREE_QUESTIONS_LIMIT) {
        openPaywallModal();
        return;
      }
      currentFilteredIndex = idx;
      renderCurrentQuestion();
    }
  }

  // Calculate stats for a given question array
  function calculateStats(qArray) {
    let total = qArray.length;
    let answered = 0;
    let correct = 0;
    let firstTry = 0;
    let subseqTry = 0;
    let inProgress = 0;
    let revealed = 0;

    qArray.forEach(q => {
      const s = userStates[q.id];
      if (!s) return;
      if (s.status === 'correct') {
        answered++;
        correct++;
        if (s.solvedOnAttempt === 1) firstTry++;
        else subseqTry++;
      } else if (s.status === 'revealed') {
        answered++;
        revealed++;
      } else if (s.status === 'in_progress') {
        inProgress++;
      }
    });

    const accuracy = answered > 0 ? Math.round((correct / answered) * 100) : 0;
    const scorePct = total > 0 ? Math.round((correct / total) * 100) : 0;
    const isPassing = (activeExamSet === 'all')
      ? (scorePct >= PASSING_THRESHOLD_PCT)
      : (correct >= PASSING_THRESHOLD_SET);

    return { total, answered, correct, firstTry, subseqTry, inProgress, revealed, accuracy, scorePct, isPassing };
  }

  // Update Header and Modal Statistics
  function updateOverallStats() {
    const currentSetStats = calculateStats(currentSetQuestions);

    headerScore.textContent = `${currentSetStats.correct} / ${currentSetStats.total}`;
    headerAccuracy.textContent = `${currentSetStats.accuracy}%`;
    headerProgress.textContent = `${currentSetStats.answered} / ${currentSetStats.total}`;

    if (gridBtnText) {
      gridBtnText.textContent = `Grid (${currentSetStats.total})`;
    }

    // Progress Bar Segments
    const pctCorrect = (currentSetStats.correct / currentSetStats.total) * 100;
    const pctInProgress = (currentSetStats.inProgress / currentSetStats.total) * 100;
    const pctRevealed = (currentSetStats.revealed / currentSetStats.total) * 100;

    pbarCorrect.style.width = `${pctCorrect}%`;
    pbarInProgress.style.width = `${pctInProgress}%`;
    pbarRevealed.style.width = `${pctRevealed}%`;

    // Modal Stat cards
    statTotalQ.textContent = currentSetStats.total;
    if (statTotalLbl) {
      statTotalLbl.textContent = activeExamSet === 'all' ? 'All Questions' : `Set ${activeExamSet} Questions`;
    }
    document.getElementById('stat-first-try').textContent = currentSetStats.firstTry;
    document.getElementById('stat-subseq-try').textContent = currentSetStats.subseqTry;
    document.getElementById('stat-revealed').textContent = currentSetStats.revealed;

    // Render Exam Status Card in Modal
    renderExamStatusCard(currentSetStats);

    // Render 4-Set Performance Matrix in Modal
    renderSetsMatrix();

    // Render Topic Mastery
    renderTopicMastery();
  }

  function renderExamStatusCard(st) {
    if (!examStatusCard) return;

    const setLabel = activeExamSet === 'all' ? 'Entire 240 Question Bank' : `Practice Exam Set ${activeExamSet} (60 Qs)`;
    examStatusTag.textContent = `${setLabel} Target`;

    if (st.answered < st.total) {
      examStatusCard.className = 'exam-status-card';
      examStatusTitle.textContent = `Current Score: ${st.correct} / ${st.total} (${st.scorePct}%)`;
      examStatusDesc.textContent = `Passing benchmark is 65% (39 / 60 correct). You have completed ${st.answered} of ${st.total} questions so far.`;
      examStatusBadge.className = 'exam-status-badge in-progress';
      examStatusBadge.textContent = `In Progress (${st.answered}/${st.total})`;
    } else if (st.isPassing) {
      examStatusCard.className = 'exam-status-card passing';
      examStatusTitle.textContent = `🎉 EXAM PASSED! (${st.correct}/${st.total} - ${st.scorePct}%)`;
      examStatusDesc.textContent = `Outstanding work! You exceeded the standard 65% Pega certification passing threshold.`;
      examStatusBadge.className = 'exam-status-badge passed';
      examStatusBadge.textContent = 'PASSED';
    } else {
      examStatusCard.className = 'exam-status-card failing';
      examStatusTitle.textContent = `⚠️ Below Passing Threshold (${st.correct}/${st.total} - ${st.scorePct}%)`;
      examStatusDesc.textContent = `You answered ${st.correct} correctly. The certification threshold requires at least 39 correct answers (65%). Review the revealed answers and retake!`;
      examStatusBadge.className = 'exam-status-badge failed';
      examStatusBadge.textContent = 'NEEDS RETAKE';
    }
  }

  function renderSetsMatrix() {
    if (!setsMatrixGrid) return;
    setsMatrixGrid.innerHTML = '';

    for (let sNum = 1; sNum <= 4; sNum++) {
      const setQs = ALL_QUESTIONS.filter(q => q.exam_set === sNum);
      const st = calculateStats(setQs);

      const card = document.createElement('div');
      card.className = `set-matrix-card ${String(sNum) === activeExamSet ? 'active-set' : ''}`;
      card.title = `Click to load Practice Exam Set ${sNum}`;

      let statusBadge = '';
      if (st.answered === 0) {
        statusBadge = '<span class="set-matrix-status">Not Started</span>';
      } else if (st.answered < 60) {
        statusBadge = `<span class="set-matrix-status">Progress: ${st.answered}/60</span>`;
      } else if (st.correct >= PASSING_THRESHOLD_SET) {
        statusBadge = `<span class="set-matrix-status pass">✅ Passed (${st.scorePct}%)</span>`;
      } else {
        statusBadge = `<span class="set-matrix-status">⚠️ ${st.scorePct}% (Needs 65%)</span>`;
      }

      card.innerHTML = `
        <div class="set-matrix-header">
          <span>Set ${sNum} (60 Qs)</span>
          ${String(sNum) === activeExamSet ? '<span style="color:var(--pega-cyan)">Active</span>' : ''}
        </div>
        <div class="set-matrix-score">${st.correct} / 60</div>
        ${statusBadge}
      `;

      card.addEventListener('click', () => {
        closeModal();
        switchExamSet(String(sNum));
      });

      setsMatrixGrid.appendChild(card);
    }
  }

  function renderTopicMastery() {
    const topicContainer = document.getElementById('topic-mastery-list');
    if (!topicContainer) return;
    topicContainer.innerHTML = '';

    const catStats = {};
    currentSetQuestions.forEach(q => {
      if (!catStats[q.category]) {
        catStats[q.category] = { total: 0, correct: 0 };
      }
      catStats[q.category].total += 1;
      const s = userStates[q.id];
      if (s && s.status === 'correct') {
        catStats[q.category].correct += 1;
      }
    });

    Object.keys(catStats).sort().forEach(cat => {
      const st = catStats[cat];
      const pct = Math.round((st.correct / st.total) * 100);

      const item = document.createElement('div');
      item.className = 'topic-item';
      item.innerHTML = `
        <div class="topic-meta">
          <span><strong>${cat}</strong> (${st.correct}/${st.total})</span>
          <span>${pct}%</span>
        </div>
        <div class="topic-bar-bg">
          <div class="topic-bar-fill" style="width: ${pct}%"></div>
        </div>
      `;
      topicContainer.appendChild(item);
    });
  }

  // Drawers and Modals
  function openDrawer() {
    questionDrawer.classList.add('active');
    drawerBackdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    questionDrawer.classList.remove('active');
    drawerBackdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  function openModal() {
    updateOverallStats();
    modalBackdrop.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modalBackdrop.style.display = 'none';
    document.body.style.overflow = '';
  }

  function openCoursesModal() {
    if (coursesModalBackdrop) {
      coursesModalBackdrop.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }
  }

  function closeCoursesModal() {
    if (coursesModalBackdrop) {
      coursesModalBackdrop.style.display = 'none';
      document.body.style.overflow = '';
    }
  }

  // Dark / Light Theme
  function loadTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === 'dark') {
      document.body.className = 'theme-dark';
      if (themeIcon) themeIcon.textContent = '☀️';
    } else {
      document.body.className = 'theme-light';
      if (themeIcon) themeIcon.textContent = '🌙';
    }
  }

  function toggleTheme() {
    if (document.body.classList.contains('theme-dark')) {
      document.body.className = 'theme-light';
      localStorage.setItem(THEME_KEY, 'light');
      if (themeIcon) themeIcon.textContent = '🌙';
    } else {
      document.body.className = 'theme-dark';
      localStorage.setItem(THEME_KEY, 'dark');
      if (themeIcon) themeIcon.textContent = '☀️';
    }
  }

  // Toast System
  function showToast(msg) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 2400);
  }

  // Event Listeners
  function attachEventListeners() {
    // Exam Set selector
    if (examSetSelect) {
      examSetSelect.addEventListener('change', (e) => {
        switchExamSet(e.target.value);
      });
    }

    // Navigation
    btnPrev.addEventListener('click', () => {
      if (currentFilteredIndex > 0) {
        currentFilteredIndex--;
        renderCurrentQuestion();
      }
    });

    btnNext.addEventListener('click', () => {
      if (!isCourseUnlocked && currentFilteredIndex >= FREE_QUESTIONS_LIMIT - 1) {
        openPaywallModal("You've completed the 7 free preview questions! Upgrade to the Full Course ($19.99 USD) to access all 240 questions across all 4 sets.");
        return;
      }
      if (currentFilteredIndex < filteredQuestions.length - 1) {
        currentFilteredIndex++;
        renderCurrentQuestion();
      }
    });

    btnSubmit.addEventListener('click', submitAnswer);

    // Shuffle controls
    btnShuffleToggle.addEventListener('click', toggleShuffle);
    btnReshuffle.addEventListener('click', reshuffleQuestions);

    // Bookmarking
    btnBookmark.addEventListener('click', () => {
      if (filteredQuestions.length === 0) return;
      const q = filteredQuestions[currentFilteredIndex];
      const qState = userStates[q.id];
      qState.bookmarked = !qState.bookmarked;
      saveUserState();
      renderCurrentQuestion();
      renderQuestionGrid();
      showToast(qState.bookmarked ? 'Question bookmarked for review ★' : 'Bookmark removed');
    });

    // Reset single question
    btnResetQ.addEventListener('click', () => {
      if (filteredQuestions.length === 0) return;
      const q = filteredQuestions[currentFilteredIndex];
      if (confirm('Reset attempts for this question?')) {
        userStates[q.id] = {
          attempts: 0,
          history: [],
          status: 'unanswered',
          bookmarked: userStates[q.id]?.bookmarked || false,
          solvedOnAttempt: null
        };
        saveUserState();
        updateOverallStats();
        renderCurrentQuestion();
        renderQuestionGrid();
        showToast('Question reset to fresh state.');
      }
    });

    // Reset all progress
    btnResetAll.addEventListener('click', () => {
      if (confirm('Are you sure you want to reset ALL practice exam progress across all sets?')) {
        ALL_QUESTIONS.forEach(q => {
          userStates[q.id] = {
            attempts: 0,
            history: [],
            status: 'unanswered',
            bookmarked: false,
            solvedOnAttempt: null
          };
        });
        saveUserState();
        updateOverallStats();
        renderCurrentQuestion();
        renderQuestionGrid();
        closeModal();
        showToast('All progress has been reset.');
      }
    });

    // Filters & Search
    categorySelect.addEventListener('change', () => applyFilters(false));
    statusFilter.addEventListener('change', () => applyFilters(false));

    searchInput.addEventListener('input', () => {
      searchClear.style.display = searchInput.value ? 'block' : 'none';
      applyFilters(false);
    });

    searchClear.addEventListener('click', () => {
      searchInput.value = '';
      searchClear.style.display = 'none';
      applyFilters(false);
    });

    // Theme toggle
    btnThemeToggle.addEventListener('click', toggleTheme);

    // Drawer
    btnGridToggle.addEventListener('click', openDrawer);
    drawerClose.addEventListener('click', closeDrawer);
    drawerBackdrop.addEventListener('click', closeDrawer);

    drawerTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        drawerTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        activeDrawerTab = tab.dataset.tab;
        renderQuestionGrid();
      });
    });

    // Modals
    btnSummaryToggle.addEventListener('click', openModal);
    modalClose.addEventListener('click', closeModal);
    btnCloseModal.addEventListener('click', closeModal);
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) closeModal();
    });

    if (btnCoursesToggle) btnCoursesToggle.addEventListener('click', openCoursesModal);
    if (brandHome) brandHome.addEventListener('click', openCoursesModal);
    if (coursesModalClose) coursesModalClose.addEventListener('click', closeCoursesModal);
    if (btnCloseCoursesModal) btnCloseCoursesModal.addEventListener('click', closeCoursesModal);
    if (btnContinueCourse1) btnContinueCourse1.addEventListener('click', closeCoursesModal);
    if (coursesModalBackdrop) {
      coursesModalBackdrop.addEventListener('click', (e) => {
        if (e.target === coursesModalBackdrop) closeCoursesModal();
      });
    }

    // Paywall Modal & Unlock Key Events
    const btnUnlockHeader = document.getElementById('btn-unlock-header');
    if (btnUnlockHeader) {
      btnUnlockHeader.addEventListener('click', () => {
        if (isCourseUnlocked) {
          showToast('⭐ Pro Access Active: You have full lifetime access to all 240 questions.');
        } else {
          openPaywallModal();
        }
      });
    }

    const btnClosePaywall = document.getElementById('btn-close-paywall');
    const paywallModalClose = document.getElementById('paywall-modal-close');
    const paywallModalBackdrop = document.getElementById('paywall-modal-backdrop');
    if (btnClosePaywall) btnClosePaywall.addEventListener('click', closePaywallModal);
    if (paywallModalClose) paywallModalClose.addEventListener('click', closePaywallModal);
    if (paywallModalBackdrop) {
      paywallModalBackdrop.addEventListener('click', (e) => {
        if (e.target === paywallModalBackdrop) closePaywallModal();
      });
    }

    const btnRedeemKey = document.getElementById('btn-redeem-key');
    const inputLicenseKey = document.getElementById('input-license-key');
    if (btnRedeemKey && inputLicenseKey) {
      btnRedeemKey.addEventListener('click', () => {
        unlockCourse(inputLicenseKey.value);
      });
      inputLicenseKey.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          unlockCourse(inputLicenseKey.value);
        }
      });
    }

    // Keyboard Shortcuts
    document.addEventListener('keydown', (e) => {
      if (document.activeElement === searchInput || (inputLicenseKey && document.activeElement === inputLicenseKey)) return;

      const key = e.key.toUpperCase();

      if (['1', '2', '3', '4'].includes(key)) {
        const idx = parseInt(key) - 1;
        selectOption(idx);
      }
      else if (['A', 'B', 'C', 'D'].includes(key)) {
        const idx = key.charCodeAt(0) - 65;
        selectOption(idx);
      }
      else if (e.key === 'Enter') {
        submitAnswer();
      }
      else if (e.key === 'ArrowLeft') {
        if (currentFilteredIndex > 0) {
          currentFilteredIndex--;
          renderCurrentQuestion();
        }
      }
      else if (e.key === 'ArrowRight') {
        if (!isCourseUnlocked && currentFilteredIndex >= FREE_QUESTIONS_LIMIT - 1) {
          openPaywallModal("You've completed the 7 free preview questions! Upgrade to the Full Course ($19.99 USD) to access all 240 questions.");
          return;
        }
        if (currentFilteredIndex < filteredQuestions.length - 1) {
          currentFilteredIndex++;
          renderCurrentQuestion();
        }
      }
      else if (key === 'R') {
        reshuffleQuestions();
      }
      else if (key === 'G') {
        if (questionDrawer.classList.contains('active')) closeDrawer();
        else openDrawer();
      }
      else if (e.key === 'Escape') {
        closeDrawer();
        closeModal();
        closeCoursesModal();
        closePaywallModal();
      }
    });
  }

  // Progressive Web App (PWA) Initialization
  function initPWA() {
    // 1. Service Worker Registration (Supports https: or localhost/127.0.0.1)
    if ('serviceWorker' in navigator && (window.location.protocol === 'https:' || window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
          .then((registration) => {
            console.log('[PWA] Service Worker registered with scope:', registration.scope);
          })
          .catch((error) => {
            console.warn('[PWA] Service Worker registration failed:', error);
          });
      });
    }

    // 2. Install App Prompt
    let deferredPrompt = null;
    const btnInstallApp = document.getElementById('btn-install-app');

    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
      if (btnInstallApp) {
        btnInstallApp.style.display = 'inline-flex';
      }
    });

    if (btnInstallApp) {
      btnInstallApp.addEventListener('click', async () => {
        if (!deferredPrompt) return;
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        console.log('[PWA] User choice outcome:', outcome);
        deferredPrompt = null;
        btnInstallApp.style.display = 'none';
      });
    }

    window.addEventListener('appinstalled', () => {
      console.log('[PWA] Application successfully installed');
      if (btnInstallApp) {
        btnInstallApp.style.display = 'none';
      }
      showToast('App installed successfully! Accessible offline from your home screen.');
    });
  }

  window.addEventListener('DOMContentLoaded', init);

})();
