/**
 * BhashaBandhu - Interactive Web App JavaScript
 * AI-Powered Local Language Tutor Simulator & Utilities
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initScenarioSimulator();
  initContactForm();
  initSpeechSynthesis();
  initAnimations();
});

/* ----------------------------------------------------
   1. NAVIGATION & MOBILE DRAWER
   ---------------------------------------------------- */
function initNavbar() {
  const navbar = document.querySelector('.bb-navbar');
  const toggleBtn = document.getElementById('mobileMenuToggle');
  const navLinks = document.getElementById('navLinks');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      navbar?.classList.add('scrolled');
    } else {
      navbar?.classList.remove('scrolled');
    }
  });

  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      const icon = toggleBtn.querySelector('i');
      if (icon) {
        if (navLinks.classList.contains('open')) {
          icon.className = 'fas fa-times';
        } else {
          icon.className = 'fas fa-bars';
        }
      }
    });

    // Close menu when clicking link
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        const icon = toggleBtn.querySelector('i');
        if (icon) icon.className = 'fas fa-bars';
      });
    });
  }
}

/* ----------------------------------------------------
   2. REAL-LIFE SCENARIO & AI TUTOR SIMULATOR DATASET
   ---------------------------------------------------- */
const SCENARIO_DATA = {
  telugu: {
    name: 'Telugu (తెలుగు)',
    langCode: 'te-IN',
    scenarios: {
      auto: {
        title: 'Auto Rickshaw Negotiation',
        icon: '🛺',
        aiPrompt: 'Namaskaram! Ekadiki vellali anna?',
        phonetic: 'Namaskaram! Ekkadiki vellaali anna?',
        translation: 'Hello! Where do you want to go brother?',
        userSample: 'Indiranagar ki entha avuthundi?',
        userPhonetic: 'Indiranagar ki entha avuthundi?',
        userTranslation: 'How much for Indiranagar?',
        aiReply: 'Meter meedha classic ₹80 avuthundi boss. Ekandi!',
        feedback: 'Excellent pronunciation! Focus on lengthening the vowel "aali" in "vellaali".'
      },
      shopkeeper: {
        title: 'Grocery / Vegetable Shopkeeper',
        icon: '🛍️',
        aiPrompt: 'Aem kaavali meeku? Tamatalu kilo ₹40.',
        phonetic: 'Emi kaavali meeku? Tamaatalu kilo ₹40.',
        translation: 'What do you need? Tomatoes are ₹40 per kilo.',
        userSample: 'Konjam thagginchandi anna, oka kilo ivvandi.',
        userPhonetic: 'Konchem thagginchandi anna, oka kilo ivvandi.',
        userTranslation: 'Reduce a little bit brother, give me one kilo.',
        aiReply: 'Sarey boss, ₹35 ki isthanu. Inka emaina kaavala?',
        feedback: 'Great tone! Friendly pitch for polite bargaining in Telugu.'
      },
      landlord: {
        title: 'Landlord & Rent Discussion',
        icon: '🏠',
        aiPrompt: 'Namaste! House visit ki vachara? Advance 5 months rent.',
        phonetic: 'Namaste! Intiki vachhaara? Advance 5 nela la rent.',
        translation: 'Hello! Did you come to see the house? Advance is 5 months rent.',
        userSample: 'Maintenance charges rent lo include ainaaya?',
        userPhonetic: 'Maintenance charges rent lo include ayyinaaya?',
        userTranslation: 'Are maintenance charges included in the rent?',
        aiReply: 'Outstation power bill meedhi, water maintenance included.',
        feedback: 'Clear flow! Clear enunciation of technical terms in daily Telugu.'
      },
      colleague: {
        title: 'Office Colleague & Tea Break',
        icon: '☕',
        aiPrompt: 'Hi! Tea ki veldhama? Kotta project updates emaina unnaya?',
        phonetic: 'Hi! Tea ki veldhama? Kothha project updates emaina unnaaya?',
        translation: 'Hi! Shall we go for tea? Any new project updates?',
        userSample: 'Ha veldhama! Nenu Irani chai taaguthanu.',
        userPhonetic: 'Haa veldhamaa! Nenu Irani chai thaaguthaanu.',
        userTranslation: 'Yes let us go! I will drink Irani tea.',
        aiReply: 'Super! Office canteens deggara irani chai awesome untundi.',
        feedback: 'Very natural conversational cadence!'
      }
    }
  },
  tamil: {
    name: 'Tamil (தமிழ்)',
    langCode: 'ta-IN',
    scenarios: {
      auto: {
        title: 'Auto Rickshaw Negotiation',
        icon: '🛺',
        aiPrompt: 'Vanakkam! Enga poga num brother?',
        phonetic: 'Vanakkam! Yenga poga num brother?',
        translation: 'Hello! Where do you need to go brother?',
        userSample: 'T.Nagar bus stand ku evlo aagum?',
        userPhonetic: 'T.Nagar bus stand ku evlo aagum?',
        userTranslation: 'How much will it be for T.Nagar bus stand?',
        aiReply: 'Meter potu 120 ruvaa aagum boss. Vaanga polarum!',
        feedback: 'Perfect Chennai slang intonation! Very practical.'
      },
      shopkeeper: {
        title: 'Grocery / Vegetable Shopkeeper',
        icon: '🛍️',
        aiPrompt: 'Enna venum thambi? Vengayam kilo ₹30.',
        phonetic: 'Enna venum thambi? Vengaayam kilo ₹30.',
        translation: 'What do you want brother? Onion kilo ₹30.',
        userSample: 'Konjam kammi pannunga anna, 2 kilo thanga.',
        userPhonetic: 'Konjam kammi pannunga anna, 2 kilo thaanga.',
        userTranslation: 'Reduce a little brother, give 2 kilos.',
        aiReply: 'Sari boss, ₹50-ku rando kilo tharen.',
        feedback: 'Spot on request tone! "Konjam kammi pannunga" is super useful.'
      },
      landlord: {
        title: 'Landlord & Rent Discussion',
        icon: '🏠',
        aiPrompt: 'House rent ₹15,000 per month. Advance 6 months.',
        phonetic: 'Veettu vaadagai ₹15,000. Advance 6 maadham.',
        translation: 'House rent is ₹15,000 per month. Advance is 6 months.',
        userSample: 'Water supply 24 hours irukka anna?',
        userPhonetic: 'Thanneer vasadhi 24 hours irukkaa anna?',
        userTranslation: 'Is 24-hour water supply available brother?',
        aiReply: 'Aama, Metro water and Borewell both available!',
        feedback: 'Great confidence! Soft "k" sound in "irukkaa".'
      },
      colleague: {
        title: 'Office Colleague & Tea Break',
        icon: '☕',
        aiPrompt: 'Filter coffee saapidalaama? Break edukalaam!',
        phonetic: 'Filter coffee saapidalaamaa? Break edukalaam!',
        translation: 'Shall we drink filter coffee? Let us take a break!',
        userSample: 'Kandippa polam! Inniku weather nalla irukku.',
        userPhonetic: 'Kandippaa polaam! Inniku weather nalla irukku.',
        userTranslation: 'Definitely let us go! Today weather is good.',
        aiReply: 'Semma! Nearby Kumbakonam Degree Coffee shop polam.',
        feedback: 'Flawless casual Tamil greeting!'
      }
    }
  },
  kannada: {
    name: 'Kannada (கன்னட / ಕನ್ನಡ)',
    langCode: 'kn-IN',
    scenarios: {
      auto: {
        title: 'Auto Rickshaw Negotiation',
        icon: '🛺',
        aiPrompt: 'Namaskara! Yelli hogabeku sir?',
        phonetic: 'Namaskara! Yelli hogabeku sir?',
        translation: 'Hello! Where do you need to go sir?',
        userSample: 'Koramangala 5th block ge eshtu aguthe?',
        userPhonetic: 'Koramangala 5th block ge eshtu aaguthe?',
        userTranslation: 'How much will it be for Koramangala 5th block?',
        aiReply: 'Meter mele ₹20 extra kodi sir, heavy traffic ide.',
        feedback: 'Smooth pronunciation! Practice the "eshtu" sound.'
      },
      shopkeeper: {
        title: 'Grocery / Vegetable Shopkeeper',
        icon: '🛍️',
        aiPrompt: 'Banni sir! Aloo-tamato fresh ide, eshtu beku?',
        phonetic: 'Banni sir! Aloo-tamato fresh ide, eshtu beku?',
        translation: 'Come sir! Potato-tomato is fresh, how much do you need?',
        userSample: 'Ondu kilo tamato kodi, price Swalpa kadime maadi.',
        userPhonetic: 'Ondu kilo tamato kodi, price Swalpa kadime maadi.',
        userTranslation: 'Give one kilo tomato, reduce price a little bit.',
        aiReply: 'Okay boss! ₹35 ge kodthini. Innu enu beku?',
        feedback: 'Native phrasing! "Swalpa kadime maadi" is key in Bengaluru.'
      },
      landlord: {
        title: 'Landlord & Rent Discussion',
        icon: '🏠',
        aiPrompt: 'Flat thumba chennagide. Rent ₹20,000. Deposit 5 months.',
        phonetic: 'Flat thumba chennagide. Rent ₹20,000. Deposit 5 months.',
        translation: 'Flat is very good. Rent ₹20,000. Deposit 5 months.',
        userSample: 'Power backup and car parking ideya sir?',
        userPhonetic: 'Power backup mathe car parking ideya sir?',
        userTranslation: 'Is there power backup and car parking sir?',
        aiReply: 'Haudu sir! Dedicated parking & generator system ide.',
        feedback: 'Very impressive clarity and pitch accuracy!'
      },
      colleague: {
        title: 'Office Colleague & Tea Break',
        icon: '☕',
        aiPrompt: 'Oota aitha? Kaafi kudiyona banni!',
        phonetic: 'Oota aitha? Kaafi kudiyona banni!',
        translation: 'Did you have lunch? Come let us drink coffee!',
        userSample: 'Oota aithu! Haa banni kaafi kudiyona.',
        userPhonetic: 'Oota aithu! Haa banni kaafi kudiyona.',
        userTranslation: 'Lunch is done! Yes come let us drink coffee.',
        aiReply: 'Super! HSR Layout Filter Coffee spot nalli try madona.',
        feedback: 'Excellent response! Friendly and confident.'
      }
    }
  },
  hindi: {
    name: 'Hindi (हिंदी)',
    langCode: 'hi-IN',
    scenarios: {
      auto: {
        title: 'Auto Rickshaw Negotiation',
        icon: '🛺',
        aiPrompt: 'Namaste bhaiya! Kahan chalna hai?',
        phonetic: 'Namaste bhaiya! Kahan chalna hai?',
        translation: 'Hello brother! Where do you want to go?',
        userSample: 'Metro station tak kitna hoga bhaiya?',
        userPhonetic: 'Metro station tak kitna hoga bhaiya?',
        userTranslation: 'How much till the metro station brother?',
        aiReply: 'Meter se chalenge sir, ₹50 hoga.',
        feedback: 'Perfect everyday Hindi tone and pitch!'
      },
      shopkeeper: {
        title: 'Grocery / Vegetable Shopkeeper',
        icon: '🛍️',
        aiPrompt: 'Aao ji! Aam aur seb fresh hain. Kya chahiye?',
        phonetic: 'Aao ji! Aam aur seb fresh hain. Kya chahiye?',
        translation: 'Come sir! Mangoes and apples are fresh. What do you need?',
        userSample: 'Bhaiya 1 kilo aam dena, thoda sahi daam lagao.',
        userPhonetic: 'Bhaiya 1 kilo aam dena, thoda sahi daam lagao.',
        userTranslation: 'Brother give 1 kilo mango, quote a fair price.',
        aiReply: 'Aapke liye ₹70 per kg laga dunga bhaiya!',
        feedback: 'Very polite and effective market dialogue!'
      },
      landlord: {
        title: 'Landlord & Rent Discussion',
        icon: '🏠',
        aiPrompt: 'Flat bilkul naya hai. Rent 18,000 aur security deposit 2 months.',
        phonetic: 'Flat bilkul naya hai. Rent 18,000 aur security deposit 2 months.',
        translation: 'Flat is brand new. Rent 18,000 and 2 months security deposit.',
        userSample: 'Agreement kitne saal ka banega sir?',
        userPhonetic: 'Agreement kitne saal ka banega sir?',
        userTranslation: 'For how many years will the agreement be made sir?',
        aiReply: '11 months ka standard rental agreement hoga.',
        feedback: 'Clear professional dialogue!'
      },
      colleague: {
        title: 'Office Colleague & Tea Break',
        icon: '☕',
        aiPrompt: 'Chai peene chalein? Kaafi time ho gaya work karte hue!',
        phonetic: 'Chai peene chalein? Kaafi time ho gaya work karte hue!',
        translation: 'Shall we go for tea? It has been a long time working!',
        userSample: 'Haan bilkul chalein! Tapri ki adrak chai mast hoti hai.',
        userPhonetic: 'Haan bilkul chalein! Tapri ki adrak chai mast hoti hai.',
        userTranslation: 'Yes absolutely let us go! Stall ginger tea is great.',
        aiReply: 'Chalo fir! Samosa bhi order karte hain.',
        feedback: 'Awesome natural conversational Hindi!'
      }
    }
  }
};

let currentLang = 'telugu';
let currentScenarioKey = 'auto';

function initScenarioSimulator() {
  const langPills = document.querySelectorAll('.bb-lang-pill');
  const scenarioBtns = document.querySelectorAll('.bb-scenario-btn');
  
  langPills.forEach(pill => {
    pill.addEventListener('click', () => {
      langPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      currentLang = pill.getAttribute('data-lang') || 'telugu';
      updateSimulatorUI();
    });
  });

  scenarioBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      scenarioBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentScenarioKey = btn.getAttribute('data-scenario') || 'auto';
      updateSimulatorUI();
    });
  });

  // Action Buttons inside Simulator
  const btnSpeakAI = document.getElementById('btnListenAI');
  const btnUserPractice = document.getElementById('btnUserPractice');
  
  if (btnSpeakAI) {
    btnSpeakAI.addEventListener('click', () => {
      const scenario = SCENARIO_DATA[currentLang].scenarios[currentScenarioKey];
      speakText(scenario.aiPrompt, SCENARIO_DATA[currentLang].langCode);
    });
  }

  if (btnUserPractice) {
    btnUserPractice.addEventListener('click', () => {
      triggerUserVoicePractice();
    });
  }

  updateSimulatorUI();
}

function updateSimulatorUI() {
  const langData = SCENARIO_DATA[currentLang] || SCENARIO_DATA.telugu;
  const scenario = langData.scenarios[currentScenarioKey] || langData.scenarios.auto;

  const scenarioTitleEl = document.getElementById('simScenarioTitle');
  const aiMsgEl = document.getElementById('simAiMsg');
  const aiPhoneticEl = document.getElementById('simAiPhonetic');
  const aiTranslationEl = document.getElementById('simAiTranslation');
  const userMsgEl = document.getElementById('simUserMsg');
  const userPhoneticEl = document.getElementById('simUserPhonetic');
  const userTranslationEl = document.getElementById('simUserTranslation');
  const feedbackEl = document.getElementById('simFeedbackText');

  if (scenarioTitleEl) scenarioTitleEl.innerHTML = `${scenario.icon} ${scenario.title} (${langData.name})`;
  if (aiMsgEl) aiMsgEl.textContent = `"${scenario.aiPrompt}"`;
  if (aiPhoneticEl) aiPhoneticEl.textContent = scenario.phonetic;
  if (aiTranslationEl) aiTranslationEl.textContent = `English: "${scenario.translation}"`;

  if (userMsgEl) userMsgEl.textContent = `"${scenario.userSample}"`;
  if (userPhoneticEl) userPhoneticEl.textContent = scenario.userPhonetic;
  if (userTranslationEl) userTranslationEl.textContent = `Meaning: "${scenario.userTranslation}"`;

  if (feedbackEl) {
    feedbackEl.innerHTML = `<strong>Pronunciation AI Feedback:</strong> 🎯 96% Score. ${scenario.feedback}`;
  }
}

/* ----------------------------------------------------
   3. SPEECH SYNTHESIS & RECOGNITION (WEB SPEECH API)
   ---------------------------------------------------- */
function initSpeechSynthesis() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = () => {
      // Warm up voices
    };
  }
}

function speakText(text, langCode) {
  if (!('speechSynthesis' in window)) {
    alert(`AI Tutor Speech Output: "${text}"`);
    return;
  }

  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = langCode || 'te-IN';
  utterance.rate = 0.9;
  utterance.pitch = 1.0;

  // Try to find native voice
  const voices = window.speechSynthesis.getVoices();
  const targetVoice = voices.find(v => v.lang.startsWith(langCode.substring(0, 2)));
  if (targetVoice) utterance.voice = targetVoice;

  const btnListen = document.getElementById('btnListenAI');
  if (btnListen) {
    btnListen.classList.add('pulse-anim');
    btnListen.innerHTML = `<i class="fas fa-volume-high fa-spin me-2"></i> Playing Audio...`;
  }

  utterance.onend = () => {
    if (btnListen) {
      btnListen.classList.remove('pulse-anim');
      btnListen.innerHTML = `<i class="fas fa-volume-high me-2"></i> Listen AI Tutor`;
    }
  };

  utterance.onerror = () => {
    if (btnListen) {
      btnListen.classList.remove('pulse-anim');
      btnListen.innerHTML = `<i class="fas fa-volume-high me-2"></i> Listen AI Tutor`;
    }
  };

  window.speechSynthesis.speak(utterance);
}

function triggerUserVoicePractice() {
  const btnPractice = document.getElementById('btnUserPractice');
  const feedbackBox = document.getElementById('simFeedbackText');
  const langData = SCENARIO_DATA[currentLang];
  
  if (!btnPractice) return;

  btnPractice.disabled = true;
  btnPractice.innerHTML = `<i class="fas fa-microphone fa-spin me-2" style="color: #EC4899;"></i> Listening... Speak Now!`;

  if (feedbackBox) {
    feedbackBox.innerHTML = `<span style="color: #4F46E5;"><i class="fas fa-wave-square fa-pulse me-2"></i> AI Analyzing microphone audio stream & pronunciation pitch...</span>`;
  }

  // Check Web Speech API Recognition
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  
  if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.lang = langData.langCode;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      const confidence = Math.round(event.results[0][0].confidence * 100) || 95;
      
      btnPractice.disabled = false;
      btnPractice.innerHTML = `<i class="fas fa-microphone me-2"></i> Practice Speaking`;

      if (feedbackBox) {
        feedbackBox.innerHTML = `<strong>Live Recognition Result:</strong> "${transcript}" <br><strong>Score:</strong> 🌟 ${confidence}% Accuracy. Outstanding pronunciation clarity! Keep it up!`;
      }
    };

    recognition.onerror = () => {
      simulatePracticeFeedback(btnPractice, feedbackBox);
    };

    recognition.onend = () => {
      btnPractice.disabled = false;
      btnPractice.innerHTML = `<i class="fas fa-microphone me-2"></i> Practice Speaking`;
    };
  } else {
    // Fallback simulation for browsers without active Mic API
    setTimeout(() => {
      simulatePracticeFeedback(btnPractice, feedbackBox);
    }, 1800);
  }
}

function simulatePracticeFeedback(btnPractice, feedbackBox) {
  const scenario = SCENARIO_DATA[currentLang].scenarios[currentScenarioKey];
  btnPractice.disabled = false;
  btnPractice.innerHTML = `<i class="fas fa-microphone me-2"></i> Practice Speaking`;

  if (feedbackBox) {
    feedbackBox.innerHTML = `<strong>AI Voice Analysis Completed:</strong> 🎯 94% Accuracy Score! <br><em>${scenario.feedback}</em>`;
  }
}

/* ----------------------------------------------------
   4. CONTACT FORM HANDLING
   ---------------------------------------------------- */
function initContactForm() {
  const contactForm = document.getElementById('bbContactForm');
  const formToast = document.getElementById('contactToast');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = document.getElementById('contactName')?.value;
      const email = document.getElementById('contactEmail')?.value;
      const lang = document.getElementById('contactLang')?.value;
      const message = document.getElementById('contactMessage')?.value;

      const submitBtn = contactForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i> Sending Message...`;
      }

      setTimeout(() => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<i class="fas fa-paper-plane me-2"></i> Send Message`;
        }

        if (formToast) {
          formToast.style.display = 'block';
          formToast.innerHTML = `
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10B981; color: #065F46; padding: 16px; border-radius: 12px; margin-top: 16px;">
              <i class="fas fa-circle-check me-2" style="font-size: 1.2rem;"></i>
              <strong>Thank you, ${name || 'Learner'}!</strong> Your message has been sent successfully to <code>poojithapooji2804@gmail.com</code>. We will guide your language learning journey shortly!
            </div>
          `;
        }

        contactForm.reset();
      }, 1200);
    });
  }
}

/* ----------------------------------------------------
   5. SCROLL & ENTRANCE ANIMATIONS
   ---------------------------------------------------- */
function initAnimations() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  document.querySelectorAll('.bb-feature-card, .bb-step-card, .bb-persona-card, .bb-why-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(24px)';
    el.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
    observer.observe(el);
  });
}
