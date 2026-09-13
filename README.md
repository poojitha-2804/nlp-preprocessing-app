# NLP Preprocess - NLP Data Preprocessing Techniques Web Application

An educational, interactive, and responsive web platform designed for students, researchers, and developers to explore, test, and understand Natural Language Processing (NLP) data preprocessing techniques.

## Key Features

- **Interactive Playground**: Real-time execution of preprocessing techniques with live comparison views.
- **Tokenization Deep Dive**: Supports 11 tokenization algorithms:
  1. Sentence Tokenization
  2. Word Tokenization
  3. Character Tokenization
  4. Subword Tokenization
  5. Whitespace Tokenization
  6. Punctuation Tokenization
  7. Regular Expression Tokenization
  8. N-gram Tokenization
  9. Byte Pair Encoding (BPE)
  10. WordPiece Tokenization
  11. Unigram Tokenization
- **Stemming Techniques**:
  1. Porter Stemmer
  2. Snowball Stemmer
  3. Lancaster Stemmer
  4. Rule-Based Stemming
  5. Lovins Stemmer
- **Lemmatization Methods**:
  1. Dictionary-Based Lemmatization
  2. Rule-Based Lemmatization
  3. WordNet Lemmatization
  4. POS-Based Lemmatization
  5. Context-Aware Lemmatization
  6. Transformer/Contextual Lemmatization
- **Stop Word Removal**:
  1. Standard English Filtering
  2. Custom Stop Word List Addition
  3. Frequency-Based Automated Stop Word Removal
  4. Domain-Specific Removal (Tech, Medical, Legal, Social Media)
  5. Language-Specific Removal (English, Spanish, French, German)
- **Text Cleaning & Normalization**:
  - Lowercasing & Uppercasing
  - Punctuation & Special Character Removal
  - Number & Extra Whitespace Removal
  - HTML Tag & URL Removal
  - Emoji Handling
  - Contraction Expansion ("don't" -> "do not")
- **Visual Analytics**:
  - Original vs. Processed text diff highlighting
  - "What happened?" explanation panel tailored to selected sub-type
  - Statistics dashboard (token counts, character counts, execution timing, words changed)

---

## Installation & Running

### 1. Prerequisites
- Python 3.9+
- Pip package manager

### 2. Create Virtual Environment & Install Dependencies
```bash
cd nlp-preprocessing-app
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Download Required NLTK Data Models (Automated on First Run)
The application automatically attempts to download standard NLTK packages (`punkt`, `wordnet`, `stopwords`, `averaged_perceptron_tagger`, `omw-1.4`) on initial startup. If you wish to pre-download them manually:
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('omw-1.4')"
```

### 4. Run the Flask Web Server
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000`.

---

## API Documentation

### Unified Processing Endpoint
- **URL**: `/api/process`
- **Method**: `POST`
- **Content-Type**: `application/json`

#### Request Payload Example:
```json
{
  "text": "Natural Language Processing is fascinating and we're learning quickly!",
  "technique": "tokenization",
  "type": "subword",
  "options": {}
}
```

#### Response Example:
```json
{
  "success": true,
  "original": "Natural Language Processing is fascinating and we're learning quickly!",
  "processed": "['Natural', 'Language', 'Process', '##ing', 'is', 'fascinat', '##ing', 'and', 'we', \"'re\", 'learn', '##ing', 'quick', '##ly', '!']",
  "output": ["Natural", "Language", "Process", "##ing", "is", "fascinat", "##ing", "and", "we", "'re", "learn", "##ing", "quick", "##ly", "!"],
  "technique": "Tokenization",
  "sub_type": "subword",
  "explanation": "Subword Tokenization decomposes words into smaller meaningful units...",
  "stats": {
    "char_count_orig": 70,
    "char_count_proc": 142,
    "word_count_orig": 9,
    "sentence_count": 1,
    "tokens_count": 15,
    "stopwords_removed": 0,
    "words_changed": 4,
    "execution_time_ms": 3.42
  }
}
```

---

## Project Structure

```
nlp-preprocessing-app/
├── app.py                      # Flask main web application & routing
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation & guide
├── utils/
│   └── nlp_processor.py        # Core NLP Processing engine & statistics
├── templates/
│   ├── layout.html             # Base layout template (Navbar, Footer, Assets)
│   ├── index.html              # Landing page
│   ├── techniques.html         # All techniques overview
│   ├── tokenization.html       # Tokenization detailed page & demo
│   ├── stemming.html           # Stemming detailed page & demo
│   ├── lemmatization.html      # Lemmatization detailed page & demo
│   ├── stopwords.html          # Stopwords detailed page & demo
│   ├── cleaning.html           # Text cleaning detailed page & demo
│   ├── playground.html         # Interactive NLP playground
│   └── about.html              # Educational & technical background
└── static/
    ├── css/
    │   └── style.css           # Custom Dark Navy / Indigo UI design
    └── js/
        ├── main.js             # General interactive script & presets
        └── playground.js       # Dynamic playground UI logic & API handling
```
