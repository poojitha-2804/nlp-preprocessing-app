/* ==========================================
   NLP PREPROCESS - PLAYGROUND INTERACTIVE JS
   ========================================== */

document.addEventListener('DOMContentLoaded', () => {
    const mainTechniqueSelect = document.getElementById('technique-select');
    const subTypeContainer = document.getElementById('sub-type-container');
    const subTypeSelect = document.getElementById('sub-type-select');
    const subTypeLabel = document.getElementById('sub-type-label');
    const customOptionsContainer = document.getElementById('custom-options-container');

    const inputTextarea = document.getElementById('playground-input');
    const processBtn = document.getElementById('process-btn');
    const clearBtn = document.getElementById('clear-btn');
    const copyBtn = document.getElementById('copy-btn');
    const presetButtons = document.querySelectorAll('.preset-btn');

    // Result UI Elements
    const resultSection = document.getElementById('result-section');
    const originalTextDisplay = document.getElementById('original-text-display');
    const processedOutputDisplay = document.getElementById('processed-output-display');
    const diffContainer = document.getElementById('diff-container');
    const explanationDisplay = document.getElementById('explanation-display');
    const techNameDisplay = document.getElementById('tech-name-display');

    // Stats Elements
    const statCharOrig = document.getElementById('stat-char-orig');
    const statCharProc = document.getElementById('stat-char-proc');
    const statWordOrig = document.getElementById('stat-word-orig');
    const statTokensProc = document.getElementById('stat-tokens-proc');
    const statSentences = document.getElementById('stat-sentences');
    const statStopwords = document.getElementById('stat-stopwords');
    const statChanges = document.getElementById('stat-changes');
    const statTime = document.getElementById('stat-time');

    // Dynamic Sub-type mappings
    const SUB_TYPES = {
        tokenization: [
            { value: 'word', label: 'Word Tokenization' },
            { value: 'sentence', label: 'Sentence Tokenization' },
            { value: 'character', label: 'Character Tokenization' },
            { value: 'subword', label: 'Subword Tokenization' },
            { value: 'whitespace', label: 'Whitespace Tokenization' },
            { value: 'punctuation', label: 'Punctuation Tokenization' },
            { value: 'regex', label: 'Regular Expression Tokenization' },
            { value: 'unigram_ngram', label: 'Unigram Tokenization (N=1)' },
            { value: 'bigram', label: 'Bigram Tokenization (N=2)' },
            { value: 'trigram', label: 'Trigram Tokenization (N=3)' },
            { value: 'ngram', label: 'N-gram Tokenization (Custom N)' },
            { value: 'bpe', label: 'Byte Pair Encoding (BPE)' },
            { value: 'wordpiece', label: 'WordPiece Tokenization' },
            { value: 'unigram', label: 'Unigram Language Model Tokenization' }
        ],
        stemming: [
            { value: 'porter', label: 'Porter Stemmer' },
            { value: 'snowball', label: 'Snowball Stemmer' },
            { value: 'lancaster', label: 'Lancaster Stemmer' },
            { value: 'rule_based', label: 'Rule-Based Stemming' },
            { value: 'lovins', label: 'Lovins Stemmer' }
        ],
        lemmatization: [
            { value: 'wordnet', label: 'WordNet Lemmatization' },
            { value: 'pos_based', label: 'POS-Based Lemmatization' },
            { value: 'context_aware', label: 'Context-Aware Lemmatization' },
            { value: 'dictionary', label: 'Dictionary-Based Lemmatization' },
            { value: 'rule_based', label: 'Rule-Based Lemmatization' }
        ],
        stopwords: [
            { value: 'standard', label: 'Standard English Stop Words' },
            { value: 'custom', label: 'Custom Stop Word Removal' },
            { value: 'frequency_based', label: 'Frequency-Based Stop Word Removal' },
            { value: 'domain_specific', label: 'Domain-Specific Stop Word Removal' },
            { value: 'language_specific', label: 'Language-Specific Stop Word Removal' }
        ],
        cleaning: [
            { value: 'all', label: 'Complete Pipeline (All Active Checks)' },
            { value: 'lowercasing', label: 'Lowercasing Only' },
            { value: 'punctuation_removal', label: 'Punctuation Removal Only' },
            { value: 'number_removal', label: 'Number Removal Only' },
            { value: 'special_character_removal', label: 'Special Character Removal Only' },
            { value: 'extra_whitespace_removal', label: 'Extra Whitespace Removal Only' },
            { value: 'html_tag_removal', label: 'HTML Tag Removal' },
            { value: 'url_removal', label: 'URL Removal' },
            { value: 'emoji_handling', label: 'Emoji Handling' },
            { value: 'contraction_expansion', label: 'Contraction Expansion' }
        ],
        pos_tagging: [
            { value: 'nltk', label: 'NLTK Perceptron POS Tagger' },
            { value: 'spacy', label: 'SpaCy Contextual POS Tagger' },
            { value: 'lexicon', label: 'Rule-Based / Lexicon POS Tagger' }
        ]
    };

    // Update Sub-Type Select Options dynamically
    function updateSubTypeDropdown() {
        const selectedTech = mainTechniqueSelect.value;
        const options = SUB_TYPES[selectedTech] || [];

        // Set Label
        if (selectedTech === 'tokenization') subTypeLabel.innerText = 'Select Tokenization Type';
        else if (selectedTech === 'stemming') subTypeLabel.innerText = 'Select Stemming Algorithm';
        else if (selectedTech === 'lemmatization') subTypeLabel.innerText = 'Select Lemmatization Method';
        else if (selectedTech === 'stopwords') subTypeLabel.innerText = 'Select Stop Word Method';
        else if (selectedTech === 'cleaning') subTypeLabel.innerText = 'Select Cleaning Operation';
        else if (selectedTech === 'pos_tagging') subTypeLabel.innerText = 'Select Tagger Engine';
        else subTypeLabel.innerText = 'Select Variant';

        subTypeSelect.innerHTML = '';
        options.forEach(opt => {
            const optionEl = document.createElement('option');
            optionEl.value = opt.value;
            optionEl.innerText = opt.label;
            subTypeSelect.appendChild(optionEl);
        });

        subTypeContainer.style.display = options.length > 0 ? 'block' : 'none';
        renderCustomOptions();
    }

    // Render extra controls based on sub-type (e.g. custom stopwords input, POS tagset select, or checkboxes)
    function renderCustomOptions() {
        const selectedTech = mainTechniqueSelect.value;
        const subType = subTypeSelect.value;
        customOptionsContainer.innerHTML = '';

        if (selectedTech === 'stopwords' && subType === 'custom') {
            customOptionsContainer.innerHTML = `
                <div class="mt-3">
                    <label class="form-label text-secondary small font-weight-bold">Custom Stop Words (comma or space separated):</label>
                    <input type="text" id="custom-words-input" class="form-control form-control-dark" placeholder="e.g. artificial, intelligence, learning, model">
                </div>
            `;
        } else if (selectedTech === 'stopwords' && subType === 'domain_specific') {
            customOptionsContainer.innerHTML = `
                <div class="mt-3">
                    <label class="form-label text-secondary small font-weight-bold">Select Domain Preset:</label>
                    <select id="domain-select" class="form-select form-select-dark">
                        <option value="tech">Technology / Programming</option>
                        <option value="medical">Healthcare / Medical</option>
                        <option value="legal">Legal / Contracts</option>
                        <option value="social">Social Media / Twitter</option>
                    </select>
                </div>
            `;
        } else if (selectedTech === 'stopwords' && subType === 'language_specific') {
            customOptionsContainer.innerHTML = `
                <div class="mt-3">
                    <label class="form-label text-secondary small font-weight-bold">Select Language:</label>
                    <select id="lang-select" class="form-select form-select-dark">
                        <option value="english">English</option>
                        <option value="spanish">Spanish</option>
                        <option value="french">French</option>
                        <option value="german">German</option>
                    </select>
                </div>
            `;
        } else if (selectedTech === 'tokenization' && subType === 'regex') {
            customOptionsContainer.innerHTML = `
                <div class="mt-3">
                    <label class="form-label text-secondary small font-weight-bold">Regex Tokenization Pattern:</label>
                    <input type="text" id="regex-pattern-input" class="form-control form-control-dark" value="\\b\\w+\\b">
                </div>
            `;
        } else if (selectedTech === 'tokenization' && subType === 'ngram') {
            customOptionsContainer.innerHTML = `
                <div class="mt-3">
                    <label class="form-label text-secondary small font-weight-bold">N-gram Count (N):</label>
                    <input type="number" id="ngram-n-input" class="form-control form-control-dark" value="2" min="1" max="5">
                </div>
            `;
        } else if (selectedTech === 'pos_tagging') {
            customOptionsContainer.innerHTML = `
                <div class="mt-3">
                    <label class="form-label text-secondary small font-weight-bold">Select Tagset Scheme:</label>
                    <select id="pos-tagset-select" class="form-select form-select-dark">
                        <option value="penn" selected>Penn Treebank Tagset (36 fine-grained tags)</option>
                        <option value="universal">Universal POS Tagset (17 coarse categories)</option>
                    </select>
                </div>
            `;
        } else if (selectedTech === 'cleaning' && subType === 'all') {
            customOptionsContainer.innerHTML = `
                <div class="mt-3">
                    <label class="form-label text-secondary small font-weight-bold mb-2">Enable / Disable Operations:</label>
                    <div class="checkbox-grid">
                        <label class="custom-checkbox-card">
                            <input type="checkbox" name="clean_op" value="lowercasing" checked> Lowercasing
                        </label>
                        <label class="custom-checkbox-card">
                            <input type="checkbox" name="clean_op" value="punctuation_removal" checked> Punctuation Removal
                        </label>
                        <label class="custom-checkbox-card">
                            <input type="checkbox" name="clean_op" value="number_removal" checked> Number Removal
                        </label>
                        <label class="custom-checkbox-card">
                            <input type="checkbox" name="clean_op" value="special_character_removal"> Special Characters
                        </label>
                        <label class="custom-checkbox-card">
                            <input type="checkbox" name="clean_op" value="extra_whitespace_removal" checked> Extra Whitespace
                        </label>
                        <label class="custom-checkbox-card">
                            <input type="checkbox" name="clean_op" value="html_tag_removal" checked> HTML Tags
                        </label>
                        <label class="custom-checkbox-card">
                            <input type="checkbox" name="clean_op" value="url_removal" checked> URLs
                        </label>
                        <label class="custom-checkbox-card">
                            <input type="checkbox" name="clean_op" value="emoji_handling" checked> Emoji Handling
                        </label>
                        <label class="custom-checkbox-card">
                            <input type="checkbox" name="clean_op" value="contraction_expansion" checked> Contraction Expansion
                        </label>
                    </div>
                </div>
            `;
        }
    }

    // Event listeners for dropdowns
    mainTechniqueSelect.addEventListener('change', updateSubTypeDropdown);
    subTypeSelect.addEventListener('change', renderCustomOptions);

    // Parse URL query parameter (e.g. ?technique=pos_tagging)
    const urlParams = new URLSearchParams(window.location.search);
    const techParam = urlParams.get('technique');
    if (techParam && mainTechniqueSelect.querySelector(`option[value="${techParam}"]`)) {
        mainTechniqueSelect.value = techParam;
    }

    // Initial setup
    updateSubTypeDropdown();

    // Process Text Action
    processBtn.addEventListener('click', async () => {
        const text = inputTextarea.value.trim();
        if (!text) {
            showToast('Please enter some text before processing.', 'error');
            return;
        }

        const technique = mainTechniqueSelect.value;
        const subType = subTypeSelect.value;

        // Extra Options
        const options = {};
        if (technique === 'stopwords' && subType === 'custom') {
            options.custom_words = document.getElementById('custom-words-input')?.value || '';
        } else if (technique === 'stopwords' && subType === 'domain_specific') {
            options.domain = document.getElementById('domain-select')?.value || 'tech';
        } else if (technique === 'stopwords' && subType === 'language_specific') {
            options.lang = document.getElementById('lang-select')?.value || 'english';
        } else if (technique === 'tokenization' && subType === 'regex') {
            options.pattern = document.getElementById('regex-pattern-input')?.value || '\\b\\w+\\b';
        } else if (technique === 'tokenization' && subType === 'ngram') {
            options.n = parseInt(document.getElementById('ngram-n-input')?.value || '2');
        } else if (technique === 'pos_tagging') {
            options.tagset = document.getElementById('pos-tagset-select')?.value || 'penn';
        } else if (technique === 'cleaning') {
            if (subType === 'all') {
                const checkboxes = document.querySelectorAll('input[name="clean_op"]:checked');
                options.operations = Array.from(checkboxes).map(cb => cb.value);
            } else {
                options.operations = [subType];
            }
        }

        processBtn.disabled = true;
        processBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Processing...';

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    technique: technique,
                    type: subType,
                    options: options
                })
            });

            const data = await response.json();
            if (!response.ok || !data.success) {
                showToast(data.error || 'Failed to process text.', 'error');
                return;
            }

            // Display Results
            resultSection.style.display = 'block';
            originalTextDisplay.innerText = data.original;

            // Formatted Processed Output
            const tagged = data.tagged_tokens || (data.pos_analysis && data.pos_analysis.tagged_tokens) || (Array.isArray(data.output) && data.output[0] && typeof data.output[0] === 'object' ? data.output : []);

            if (technique === 'pos_tagging' || data.technique === 'POS Tagging') {
                if (tagged.length > 0) {
                    processedOutputDisplay.innerText = tagged.map(t => `${t.token}/${t.tag} (${t.category})`).join('  ');
                } else {
                    processedOutputDisplay.innerText = data.processed || data.output;
                }
            } else if (technique === 'lemmatization' || data.technique === 'Lemmatization') {
                if (Array.isArray(data.output)) {
                    processedOutputDisplay.innerText = data.output.map((lemma, idx) => {
                        const posItem = tagged[idx] || {};
                        const cat = posItem.category || '';
                        return cat ? `${lemma} (${cat})` : lemma;
                    }).join('  ');
                } else {
                    processedOutputDisplay.innerText = data.processed || data.output;
                }
            } else if (Array.isArray(data.output)) {
                if (data.output[0] && typeof data.output[0] === 'object' && data.output[0].token) {
                    processedOutputDisplay.innerText = data.output.map(t => `${t.token}/${t.tag} (${t.category || ''})`).join('  ');
                } else {
                    processedOutputDisplay.innerText = data.output.join('  ');
                }
            } else {
                processedOutputDisplay.innerText = data.processed || data.output;
            }

            // Explanation & Title
            techNameDisplay.innerText = `${data.technique} (${data.sub_type.replace(/_/g, ' ')})`;
            explanationDisplay.innerText = data.explanation;

            // Render POS Tag Visual Badges Container if POS Tagging or Lemmatization active
            const posContainer = document.getElementById('pos-visual-container');
            const posContent = document.getElementById('pos-badges-content');
            const taggedTokens = data.tagged_tokens || (data.pos_analysis && data.pos_analysis.tagged_tokens) || (Array.isArray(data.output) && data.output[0] && data.output[0].token ? data.output : null);

            if (posContainer && posContent && taggedTokens && taggedTokens.length > 0) {
                posContainer.style.display = 'block';
                posContent.innerHTML = taggedTokens.map(item => `
                    <div class="d-inline-flex flex-column align-items-center p-2 rounded bg-black border border-secondary shadow-sm" style="min-width: 75px;" title="${item.desc || item.category}">
                        <span class="badge ${item.badge || 'bg-primary'} mb-1" style="font-size: 0.7rem; background-color: ${item.color || ''} !important;">
                            ${item.tag} &bull; ${item.category}
                        </span>
                        <span class="fs-6 fw-bold text-white">${item.token}</span>
                    </div>
                `).join('');
            } else if (posContainer) {
                posContainer.style.display = 'none';
            }

            // Render Python Code Snippet
            const pyDisplay = document.getElementById('python-code-display');
            if (pyDisplay && data.python_code) {
                pyDisplay.innerText = data.python_code;
            }

            // Render Token Frequency Distribution
            const freqDisplay = document.getElementById('freq-container');
            if (freqDisplay && Array.isArray(data.token_freq) && data.token_freq.length > 0) {
                freqDisplay.innerHTML = data.token_freq.map(item => 
                    `<span class="badge badge-technique me-1 mb-1">${item.token}: <strong>${item.count}</strong></span>`
                ).join(' ');
            } else if (freqDisplay) {
                freqDisplay.innerText = 'Frequency counts calculated after processing.';
            }

            // Render Multi-step Pipeline Stages if active
            const pipeContainer = document.getElementById('pipeline-stages-container');
            const pipeContent = document.getElementById('pipeline-stages-content');
            if (data.is_pipeline && Array.isArray(data.pipeline_stages)) {
                pipeContainer.style.display = 'block';
                pipeContent.innerHTML = data.pipeline_stages.map(stg => `
                    <div class="p-2 mb-2 glass-card small border-success">
                        <div class="fw-bold text-success">Stage ${stg.stage}: ${stg.name}</div>
                        <div class="font-monospace text-dark text-break">${Array.isArray(stg.output) ? JSON.stringify(stg.output) : stg.output}</div>
                    </div>
                `).join('');
            } else if (pipeContainer) {
                pipeContainer.style.display = 'none';
            }

            // Render Diff Comparison
            renderDiffView(data);

            // Render Statistics
            renderStats(data.stats);

            // Save active output data for export
            window.latestOutputData = data;

            // Scroll smoothly to result section
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        } catch (err) {
            showToast(`Error: ${err.message}`, 'error');
        } finally {
            processBtn.disabled = false;
            processBtn.innerHTML = '<i class="fas fa-play me-2"></i> Process Text';
        }
    });

    // Diff Chip View Rendering
    function renderDiffView(data) {
        if (!diffContainer) return;
        diffContainer.innerHTML = '';

        if (Array.isArray(data.removed_words) && data.removed_words.length > 0) {
            const removedSet = new Set(data.removed_words.map(w => w.lower ? w.lower() : w));
            const words = data.original.split(/\s+/);
            diffContainer.innerHTML = words.map(w => {
                const clean = w.replace(/[^\w]/g, '').toLowerCase();
                if (removedSet.has(clean)) {
                    return `<span class="token-chip removed">${w}</span>`;
                } else {
                    return `<span class="token-chip">${w}</span>`;
                }
            }).join(' ');
            return;
        }

        if (Array.isArray(data.diff) && data.diff.length > 0) {
            const tagged = data.tagged_tokens || (data.pos_analysis && data.pos_analysis.tagged_tokens) || [];
            diffContainer.innerHTML = data.diff.map((item, idx) => {
                const posItem = tagged[idx] || {};
                const cat = posItem.category ? `<small class="text-cyan ms-1">(${posItem.category})</small>` : '';
                if (item.changed) {
                    return `<span class="token-chip changed" title="Transformed">${item.original} &rarr; ${item.processed} ${cat}</span>`;
                } else {
                    return `<span class="token-chip">${item.original} ${cat}</span>`;
                }
            }).join(' ');
            return;
        }

        if (Array.isArray(data.output)) {
            diffContainer.innerHTML = data.output.map(token => {
                if (typeof token === 'object' && token.token) {
                    return `<span class="token-chip">${token.token} <small class="text-cyan">(${token.category || token.tag})</small></span>`;
                }
                return `<span class="token-chip">${token}</span>`;
            }).join(' ');
        } else {
            diffContainer.innerText = data.processed;
        }
    }

    // Stats Rendering
    function renderStats(stats) {
        if (!stats) return;
        if (statCharOrig) statCharOrig.innerText = stats.char_count_orig ?? '-';
        if (statCharProc) statCharProc.innerText = stats.char_count_proc ?? '-';
        if (statWordOrig) statWordOrig.innerText = stats.word_count_orig ?? '-';
        if (statTokensProc) statTokensProc.innerText = stats.tokens_count ?? '-';
        if (statSentences) statSentences.innerText = stats.sentence_count ?? '-';
        if (statStopwords) statStopwords.innerText = stats.stopwords_removed ?? '0';
        if (statChanges) statChanges.innerText = stats.words_changed ?? '0';
        if (statTime) statTime.innerText = `${stats.execution_time_ms ?? '0'} ms`;
    }

    // Clear Input
    clearBtn.addEventListener('click', () => {
        inputTextarea.value = '';
        resultSection.style.display = 'none';
        showToast('Playground cleared.', 'info');
    });

    // Copy Output
    copyBtn.addEventListener('click', () => {
        copyToClipboard('processed-output-display');
    });

    // Copy Python Code Button
    document.getElementById('copy-python-btn')?.addEventListener('click', () => {
        copyToClipboard('python-code-display');
    });

    // Download JSON Dataset Button
    document.getElementById('download-json-btn')?.addEventListener('click', () => {
        if (!window.latestOutputData) {
            showToast('No processed dataset to download.', 'error');
            return;
        }
        const blob = new Blob([JSON.stringify(window.latestOutputData, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `svcet_nlp_dataset_${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
        showToast('JSON dataset downloaded!', 'success');
    });

    // Download CSV Dataset Button
    document.getElementById('download-csv-btn')?.addEventListener('click', () => {
        if (!window.latestOutputData || !Array.isArray(window.latestOutputData.output)) {
            showToast('No token array dataset to export to CSV.', 'error');
            return;
        }
        const tokens = window.latestOutputData.output;
        let csvContent = "Index,Token\n" + tokens.map((t, idx) => {
            const val = typeof t === 'object' ? `${t.token} (${t.tag})` : String(t);
            return `${idx + 1},"${val.replace(/"/g, '""')}"`;
        }).join("\n");
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `svcet_nlp_tokens_${Date.now()}.csv`;
        a.click();
        URL.revokeObjectURL(url);
        showToast('CSV dataset downloaded!', 'success');
    });

    // Preset Sample Text Buttons
    presetButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const sampleText = btn.getAttribute('data-sample');
            if (sampleText) {
                inputTextarea.value = sampleText;
                showToast('Sample text loaded!', 'success');
            }
        });
    });
});
