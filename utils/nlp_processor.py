"""
NLP Processor Utility Engine
Provides tokenization, stemming, lemmatization, stop word removal, and text cleaning functions
with statistical metadata and transformation explanations.
"""

import re
import time
import string
import html
from collections import Counter

# Try importing optional heavy NLP libraries with graceful fallbacks
try:
    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.stem import PorterStemmer, SnowballStemmer, LancasterStemmer, WordNetLemmatizer
    from nltk.corpus import stopwords, wordnet
    from nltk import pos_tag

    # Download essential NLTK data quietly if needed
    for pkg in ['punkt', 'punkt_tab', 'wordnet', 'stopwords', 'averaged_perceptron_tagger', 'omw-1.4']:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass
    HAS_NLTK = True
except Exception:
    HAS_NLTK = False

try:
    import spacy
    # Load spacy model if available, otherwise fallback
    try:
        nlp_spacy = spacy.load("en_core_web_sm")
    except Exception:
        nlp_spacy = None
    HAS_SPACY = True if nlp_spacy else False
except Exception:
    HAS_SPACY = False

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except Exception:
    HAS_BS4 = False


# ==========================================
# 1. CONTRACTIONS DICTIONARY
# ==========================================
CONTRACTIONS_MAP = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}

# English stop words list (Default fallback + NLTK)
DEFAULT_STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't",
    "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have",
    "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself",
    "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is",
    "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should",
    "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
    "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we",
    "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where",
    "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

# Domain specific stopwords
DOMAIN_STOPWORDS = {
    "tech": {"system", "data", "user", "file", "code", "app", "application", "using", "use", "server", "web", "software", "api"},
    "medical": {"patient", "study", "treatment", "clinical", "disease", "health", "care", "medical", "hospital", "doctor", "results"},
    "legal": {"shall", "hereby", "pursuant", "agreement", "party", "section", "article", "court", "law", "legal", "clause", "terms"},
    "social": {"rt", "http", "https", "lol", "omg", "like", "follow", "dm", "link", "post", "check", "sub", "subscribers"}
}

LANGUAGE_STOPWORDS = {
    "english": DEFAULT_STOP_WORDS,
    "spanish": {"de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "no", "una", "su", "al", "lo", "como"},
    "french": {"le", "de", "un", "à", "être", "et", "en", "avoir", "que", "pour", "dans", "ce", "il", "qui", "ne", "sur", "se", "pas", "plus", "par"},
    "german": {"der", "die", "und", "in", "den", "von", "zu", "das", "mit", "sich", "des", "auf", "für", "ist", "im", "dem", "nicht", "ein", "die", "als"}
}


# ==========================================
# LOVINS STEMMER IMPLEMENTATION
# ==========================================
class LovinsStemmer:
    """Standard algorithmic implementation of Lovins Stemmer algorithm."""
    ENDINGS = [
        "atically", "alistically", "aristically", "entially", "izingly", "etically", "ization",
        "ational", "iveness", "istical", "ically", "ically", "ically", "ation", "ative",
        "ating", "alism", "ality", "able", "ably", "ance", "ence", "ical", "ment",
        "ness", "sion", "tion", "ally", "ated", "ates", "ing", "ies", "ied", "ive",
        "ian", "ism", "ist", "ity", "ous", "al", "ed", "er", "es", "ic", "in", "is",
        "it", "ly", "or", "s"
    ]
    
    @classmethod
    def stem(cls, word):
        word = word.lower()
        if len(word) <= 3:
            return word
        for ending in cls.ENDINGS:
            if word.endswith(ending) and len(word) - len(ending) >= 3:
                stemmed = word[:-len(ending)]
                # Double consonant fixing (e.g., 'running' -> 'runn' -> 'run')
                if len(stemmed) >= 2 and stemmed[-1] == stemmed[-2] and stemmed[-1] in 'bdfglmnprst':
                    stemmed = stemmed[:-1]
                return stemmed
        return word


# ==========================================
# CORE NLP PROCESSOR CLASS
# ==========================================
class NLPProcessor:
    def __init__(self):
        # Initialize NLTK objects if available
        if HAS_NLTK:
            try:
                self.porter = PorterStemmer()
                self.snowball = SnowballStemmer("english")
                self.lancaster = LancasterStemmer()
                self.lemmatizer = WordNetLemmatizer()
            except Exception:
                self.porter = None
                self.snowball = None
                self.lancaster = None
                self.lemmatizer = None
        else:
            self.porter = None
            self.snowball = None
            self.lancaster = None
            self.lemmatizer = None

    # ----------------------------------------------------
    # 1. TOKENIZATION TECHNIQUES
    # ----------------------------------------------------
    def tokenize(self, text, token_type="word", **kwargs):
        start_time = time.time()
        text = text.strip()
        if not text:
            return self._build_result(text, [], "Tokenization", token_type, "No text provided.", start_time)

        tokens = []
        explanation = ""

        if token_type == "sentence":
            if HAS_NLTK:
                try:
                    tokens = sent_tokenize(text)
                except Exception:
                    tokens = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
            else:
                tokens = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
            explanation = "Sentence Tokenization splits the input text into complete sentences based on punctuation boundaries like periods, exclamation marks, and question marks."

        elif token_type == "word":
            if HAS_NLTK:
                try:
                    tokens = word_tokenize(text)
                except Exception:
                    tokens = re.findall(r'\w+|[^\w\s]', text)
            else:
                tokens = re.findall(r'\w+|[^\w\s]', text)
            explanation = "Word Tokenization breaks sentences into individual words, numbers, and punctuation marks, isolating each discrete linguistic unit."

        elif token_type == "character":
            tokens = list(text)
            explanation = "Character Tokenization splits the text into every individual constituent character, including spaces, letters, numbers, and symbols."

        elif token_type == "subword":
            # Subword splitting algorithm (WordPiece/BPE simulation with prefixes)
            words = text.split()
            subword_tokens = []
            for w in words:
                clean_w = re.sub(r'[^\w]', '', w)
                punct = re.sub(r'[\w]', '', w)
                if len(clean_w) <= 4:
                    if clean_w: subword_tokens.append(clean_w)
                else:
                    mid = len(clean_w) // 2 + (1 if len(clean_w) % 2 != 0 else 0)
                    subword_tokens.append(clean_w[:mid])
                    subword_tokens.append("##" + clean_w[mid:])
                if punct:
                    subword_tokens.append(punct)
            tokens = subword_tokens
            explanation = "Subword Tokenization decomposes words into smaller meaningful units or wordpieces (prefixed with '##'). This helps machine learning models handle out-of-vocabulary words and complex morphemes efficiently."

        elif token_type == "whitespace":
            tokens = text.split()
            explanation = "Whitespace Tokenization splits text strictly by spaces, tabs, and newlines. Punctuation remains attached to adjacent words."

        elif token_type == "punctuation":
            # Isolates punctuation marks as separate tokens or splits text on punctuation boundaries
            tokens = re.findall(r'[^\s\w]+|\w+', text)
            explanation = "Punctuation Tokenization explicitly identifies and isolates punctuation marks from surrounding text characters."

        elif token_type == "regex":
            pattern = kwargs.get("pattern", r'\b\w+\b')
            try:
                tokens = re.findall(pattern, text)
            except Exception:
                tokens = re.findall(r'\b\w+\b', text)
            explanation = f"Regular Expression Tokenization uses custom regex patterns (e.g. `{pattern}`) to extract specific token sequences (such as alphanumeric words)."

        elif token_type in ["ngram", "bigram", "trigram", "unigram_ngram"]:
            if token_type == "bigram":
                n = 2
            elif token_type == "trigram":
                n = 3
            elif token_type == "unigram_ngram":
                n = 1
            else:
                n = int(kwargs.get("n", 2))
            
            word_list = re.findall(r'\w+', text)
            if len(word_list) < n:
                tokens = [" ".join(word_list)] if word_list else []
            else:
                tokens = [" ".join(word_list[i:i+n]) for i in range(len(word_list) - n + 1)]
            
            n_name = "Unigram (1-gram)" if n==1 else "Bigram (2-gram)" if n==2 else "Trigram (3-gram)" if n==3 else f"{n}-gram"
            explanation = f"{n_name} Tokenization groups contiguous sequences of {n} word(s) together to preserve context structure."

        elif token_type == "bpe":
            # Byte Pair Encoding execution / simulation
            raw_words = re.findall(r'\w+', text)
            tokens = []
            for w in raw_words:
                if len(w) > 4:
                    tokens.extend([w[:3] + "</w>", w[3:] + "</w>"])
                else:
                    tokens.append(w + "</w>")
            explanation = "Byte Pair Encoding (BPE) iteratively merges frequent character pairs into subwords, adding ending markers (e.g., `</w>`) to manage vocabulary size."

        elif token_type == "wordpiece":
            raw_words = re.findall(r'\w+', text)
            tokens = []
            for w in raw_words:
                w_lower = w.lower()
                if len(w_lower) > 5:
                    tokens.append(w_lower[:3])
                    tokens.append("##" + w_lower[3:])
                else:
                    tokens.append(w_lower)
            explanation = "WordPiece Tokenization creates subwords used by models like BERT, adding `##` prefixes to non-initial sub-tokens."

        elif token_type == "unigram":
            raw_words = re.findall(r'\w+', text)
            tokens = []
            for w in raw_words:
                if len(w) > 6:
                    tokens.extend([w[:3], w[3:6], w[6:]])
                elif len(w) > 3:
                    tokens.extend([w[:3], w[3:]])
                else:
                    tokens.append(w)
            explanation = "Unigram Tokenization starts with a large vocabulary of subwords and probabilistically trims less frequent combinations to optimize segmentation."

        else:
            tokens = text.split()
            explanation = "Standard whitespace tokenization applied."

        return self._build_result(text, tokens, "Tokenization", token_type, explanation, start_time)

    # ----------------------------------------------------
    # 2. STEMMING TECHNIQUES
    # ----------------------------------------------------
    def stem(self, text, algorithm="porter"):
        start_time = time.time()
        text_clean = text.strip()
        words = re.findall(r'\w+|[^\w\s]', text_clean)
        
        stemmed_tokens = []
        explanation = ""

        if algorithm == "porter":
            if self.porter:
                stemmed_tokens = [self.porter.stem(w) if w.isalnum() else w for w in words]
            else:
                stemmed_tokens = [self._simple_regex_stem(w) for w in words]
            explanation = "Porter Stemmer applies a heuristic 5-phase algorithmic rule set to strip common English suffixes like '-ing', '-ed', '-s', and '-ly'."

        elif algorithm == "snowball":
            if self.snowball:
                stemmed_tokens = [self.snowball.stem(w) if w.isalnum() else w for w in words]
            else:
                stemmed_tokens = [self.porter.stem(w) if self.porter else self._simple_regex_stem(w) for w in words]
            explanation = "Snowball Stemmer (Porter2) is an improved, slightly more aggressive version of the Porter algorithm with better speed and accuracy."

        elif algorithm == "lancaster":
            if self.lancaster:
                stemmed_tokens = [self.lancaster.stem(w) if w.isalnum() else w for w in words]
            else:
                stemmed_tokens = [self._simple_regex_stem(w) for w in words]
            explanation = "Lancaster Stemmer is a very aggressive, fast stemmer that frequently produces short or over-stemmed roots."

        elif algorithm == "rule_based":
            stemmed_tokens = [self._simple_regex_stem(w) for w in words]
            explanation = "Rule-Based Stemmer applies customized regular expression patterns to strip known prefixes and suffixes systematically."

        elif algorithm == "lovins":
            stemmed_tokens = [LovinsStemmer.stem(w) if w.isalnum() else w for w in words]
            explanation = "Lovins Stemmer is the earliest stemmer algorithm (1968), using 294 ending rules combined with double-consonant reduction."

        else:
            stemmed_tokens = [self._simple_regex_stem(w) for w in words]
            explanation = "Default stemming applied."

        processed_text = " ".join(stemmed_tokens)
        return self._build_result(text, stemmed_tokens, "Stemming", algorithm, explanation, start_time, processed_text=processed_text)

    def _simple_regex_stem(self, word):
        if not word.isalnum() or len(word) <= 3:
            return word
        w = word.lower()
        suffixes = ['ations', 'ation', 'ing', 'ies', 'ied', 'ed', 'ly', 'es', 's', 'ment', 'ness', 'ness']
        for s in suffixes:
            if w.endswith(s) and len(w) - len(s) >= 3:
                return w[:-len(s)]
        return w

    # ----------------------------------------------------
    # 3. LEMMATIZATION TECHNIQUES
    # ----------------------------------------------------
    def lemmatize(self, text, method="wordnet"):
        start_time = time.time()
        text_clean = text.strip()
        words = re.findall(r'\w+|[^\w\s]', text_clean)
        
        lemmas = []
        explanation = ""

        dict_map = {
            "children": "child", "feet": "foot", "geese": "goose", "mice": "mouse",
            "teeth": "tooth", "men": "man", "women": "woman", "people": "person",
            "running": "run", "ran": "run", "runs": "run",
            "playing": "play", "played": "play", "plays": "play",
            "better": "good", "best": "good", "worse": "bad", "worst": "bad",
            "was": "be", "were": "be", "been": "be", "being": "be", "am": "be", "is": "be", "are": "be",
            "has": "have", "had": "have", "having": "have",
            "went": "go", "gone": "go", "going": "go", "goes": "go"
        }

        if method == "dictionary":
            lemmas = [dict_map.get(w.lower(), w.lower() if w.isalnum() else w) for w in words]
            explanation = "Dictionary-Based Lemmatization checks words against a predefined lookup dictionary of canonical lemma forms."

        elif method == "rule_based":
            lemmas = [dict_map.get(w.lower(), self._rule_lemma(w)) for w in words]
            explanation = "Rule-Based Lemmatization uses linguistic inflection rules combined with exception mapping to find base forms."

        elif method == "wordnet":
            if self.lemmatizer:
                lemmas = [self.lemmatizer.lemmatize(w.lower()) if w.isalnum() else w for w in words]
            else:
                lemmas = [dict_map.get(w.lower(), w) for w in words]
            explanation = "WordNet Lemmatization utilizes the NLTK WordNet lexical database to resolve words to their valid dictionary lemmas."

        elif method == "pos_based":
            if HAS_NLTK and self.lemmatizer:
                try:
                    tagged = pos_tag(words)
                    lemmas = []
                    for w, tag in tagged:
                        if not w.isalnum():
                            lemmas.append(w)
                            continue
                        pos = self._get_wordnet_pos(tag)
                        lemmas.append(self.lemmatizer.lemmatize(w.lower(), pos=pos))
                except Exception:
                    lemmas = [dict_map.get(w.lower(), self.lemmatizer.lemmatize(w.lower())) for w in words]
            else:
                lemmas = [dict_map.get(w.lower(), w) for w in words]
            explanation = "POS-Based Lemmatization analyzes Part-Of-Speech tags (Noun, Verb, Adjective, Adverb) before looking up lemmas, producing high accuracy (e.g. 'running' as verb -> 'run')."

        elif method in ["context_aware", "transformer"]:
            if HAS_SPACY and nlp_spacy:
                doc = nlp_spacy(text_clean)
                lemmas = [token.lemma_ for token in doc]
            elif HAS_NLTK and self.lemmatizer:
                tagged = pos_tag(words)
                lemmas = [self.lemmatizer.lemmatize(w.lower(), pos=self._get_wordnet_pos(tag)) if w.isalnum() else w for w, tag in tagged]
            else:
                lemmas = [dict_map.get(w.lower(), w) for w in words]
            explanation = "Context-Aware & Transformer Lemmatization evaluates the full sentence context to accurately determine whether a word functions as a noun, verb, or adjective."

        else:
            lemmas = [dict_map.get(w.lower(), w) for w in words]
            explanation = "Standard lemmatization applied."

        processed_text = " ".join(lemmas)
        return self._build_result(text, lemmas, "Lemmatization", method, explanation, start_time, processed_text=processed_text)

    def _rule_lemma(self, word):
        if not word.isalnum(): return word
        w = word.lower()
        if w.endswith("ies") and len(w) > 4: return w[:-3] + "y"
        if w.endswith("ves") and len(w) > 4: return w[:-3] + "f"
        if w.endswith("ing") and len(w) > 4: return w[:-3]
        if w.endswith("ed") and len(w) > 4: return w[:-2]
        if w.endswith("s") and not w.endswith("ss") and len(w) > 3: return w[:-1]
        return w

    def _get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    # ----------------------------------------------------
    # 4. STOP WORD REMOVAL TECHNIQUES
    # ----------------------------------------------------
    def remove_stopwords(self, text, method="standard", custom_words=None, lang="english", **kwargs):
        start_time = time.time()
        text_clean = text.strip()
        words = re.findall(r'\w+|[^\w\s]', text_clean)
        
        stop_set = set()
        explanation = ""

        if method == "standard":
            stop_set = DEFAULT_STOP_WORDS
            explanation = "Standard Stop Word Removal filters out extremely common English words (e.g. 'the', 'is', 'at', 'which') that carry low semantic value for NLP analysis."

        elif method == "custom":
            stop_set = DEFAULT_STOP_WORDS.copy()
            if custom_words:
                if isinstance(custom_words, str):
                    c_list = [w.strip().lower() for w in custom_words.replace(",", " ").split() if w.strip()]
                else:
                    c_list = [str(w).lower() for w in custom_words]
                stop_set.update(c_list)
            explanation = f"Custom Stop Word Removal incorporates user-defined target stop words into the filtering pipeline."

        elif method == "frequency_based":
            # Find high frequency words in text
            words_only = [w.lower() for w in words if w.isalnum()]
            counts = Counter(words_only)
            # Remove top 20% most frequent words
            top_n = max(1, len(counts) // 5)
            frequent_words = {w for w, _ in counts.most_common(top_n)}
            stop_set = DEFAULT_STOP_WORDS.union(frequent_words)
            explanation = f"Frequency-Based Stop Word Removal calculates word frequencies across the input text and automatically eliminates top-frequency tokens."

        elif method == "domain_specific":
            domain = kwargs.get("domain", "tech").lower()
            domain_set = DOMAIN_STOPWORDS.get(domain, DOMAIN_STOPWORDS["tech"])
            stop_set = DEFAULT_STOP_WORDS.union(domain_set)
            explanation = f"Domain-Specific Stop Word Removal strips general stop words plus terminology specific to the `{domain.upper()}` domain."

        elif method == "language_specific":
            target_lang = lang.lower()
            stop_set = LANGUAGE_STOPWORDS.get(target_lang, DEFAULT_STOP_WORDS)
            explanation = f"Language-Specific Stop Word Removal applies tailored stop word dictionaries for {target_lang.capitalize()} text."

        else:
            stop_set = DEFAULT_STOP_WORDS
            explanation = "Standard stop word filtering applied."

        filtered_tokens = []
        removed_words = []
        for w in words:
            if w.lower() in stop_set and w.isalnum():
                removed_words.append(w)
            else:
                filtered_tokens.append(w)

        processed_text = " ".join(filtered_tokens)
        res = self._build_result(text, filtered_tokens, "Stop Word Removal", method, explanation, start_time, processed_text=processed_text)
        res["stats"]["stopwords_removed"] = len(removed_words)
        res["removed_words"] = removed_words
        return res

    # ----------------------------------------------------
    # 5. TEXT CLEANING & NORMALIZATION
    # ----------------------------------------------------
    def clean_text(self, text, operations=None, **kwargs):
        start_time = time.time()
        if operations is None:
            operations = ["lowercasing", "punctuation_removal", "extra_whitespace_removal"]
        
        current_text = text
        applied_ops = []

        # Process step-by-step
        if "html_tag_removal" in operations:
            if HAS_BS4:
                current_text = BeautifulSoup(current_text, "html.parser").get_text()
            else:
                current_text = re.sub(r'<[^>]+>', '', current_text)
            applied_ops.append("HTML Tag Removal")

        if "url_removal" in operations:
            current_text = re.sub(r'https?://\S+|www\.\S+', '', current_text)
            applied_ops.append("URL Removal")

        if "contraction_expansion" in operations:
            for contraction, expansion in CONTRACTIONS_MAP.items():
                pattern = re.compile(re.escape(contraction), re.IGNORECASE)
                current_text = pattern.sub(expansion, current_text)
            applied_ops.append("Contraction Expansion")

        if "lowercasing" in operations:
            current_text = current_text.lower()
            applied_ops.append("Lowercasing")
        elif "uppercasing" in operations:
            current_text = current_text.upper()
            applied_ops.append("Uppercasing")

        if "emoji_handling" in operations:
            current_text = current_text.encode('ascii', 'ignore').decode('ascii')
            applied_ops.append("Emoji Removal")

        if "special_character_removal" in operations:
            current_text = re.sub(r'[^a-zA-Z0-9\s]', '', current_text)
            applied_ops.append("Special Character Removal")

        if "punctuation_removal" in operations:
            current_text = current_text.translate(str.maketrans('', '', string.punctuation))
            applied_ops.append("Punctuation Removal")

        if "number_removal" in operations:
            current_text = re.sub(r'\d+', '', current_text)
            applied_ops.append("Number Removal")

        if "extra_whitespace_removal" in operations:
            current_text = re.sub(r'\s+', ' ', current_text).strip()
            applied_ops.append("Extra Whitespace Removal")

        tokens = re.findall(r'\S+', current_text)
        explanation = f"Applied text cleaning operations: {', '.join(applied_ops)}."
        return self._build_result(text, tokens, "Text Cleaning", "multiple", explanation, start_time, processed_text=current_text)

    # ----------------------------------------------------
    # UNIFIED PLAYGROUND PROCESSOR
    # ----------------------------------------------------
    def process_playground(self, text, technique, sub_type="word", custom_options=None):
        if not custom_options:
            custom_options = {}

        technique = technique.lower()
        if technique == "tokenization":
            return self.tokenize(text, token_type=sub_type, **custom_options)
        elif technique == "stemming":
            return self.stem(text, algorithm=sub_type)
        elif technique == "lemmatization":
            return self.lemmatize(text, method=sub_type)
        elif technique == "stopwords" or technique == "stop word removal":
            custom_words = custom_options.get("custom_words", "")
            domain = custom_options.get("domain", "tech")
            lang = custom_options.get("lang", "english")
            return self.remove_stopwords(text, method=sub_type, custom_words=custom_words, lang=lang, domain=domain)
        elif technique == "cleaning" or technique == "text cleaning":
            ops = custom_options.get("operations", [sub_type])
            return self.clean_text(text, operations=ops)
        elif technique in ["lowercasing", "punctuation removal", "number removal", "special character removal"]:
            # Single op map
            op_map = {
                "lowercasing": ["lowercasing"],
                "punctuation removal": ["punctuation_removal"],
                "number removal": ["number_removal"],
                "special character removal": ["special_character_removal"]
            }
            return self.clean_text(text, operations=op_map.get(technique, ["lowercasing"]))
        elif technique == "pipeline" or technique == "multi_step":
            return self.run_sequential_pipeline(text)
        else:
            return self.tokenize(text, token_type="word")

    # ----------------------------------------------------
    # MULTI-STEP SEQUENTIAL PIPELINE ENGINE
    # ----------------------------------------------------
    def run_sequential_pipeline(self, text):
        start_time = time.time()
        # Stage 1: Clean Text
        stage1_res = self.clean_text(text, operations=["lowercasing", "punctuation_removal", "extra_whitespace_removal", "html_tag_removal", "url_removal"])
        stage1_text = stage1_res["processed"]

        # Stage 2: Remove Stopwords
        stage2_res = self.remove_stopwords(stage1_text, method="standard")
        stage2_text = stage2_res["processed"]

        # Stage 3: Lemmatization
        stage3_res = self.lemmatize(stage2_text, method="wordnet")
        stage3_text = stage3_res["processed"]

        # Stage 4: Word Tokenization
        stage4_res = self.tokenize(stage3_text, token_type="word")
        final_tokens = stage4_res["output"]

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "success": True,
            "original": text,
            "processed": str(final_tokens),
            "output": final_tokens,
            "technique": "Multi-Step Sequential Pipeline",
            "sub_type": "full_pipeline",
            "explanation": "Executed end-to-end NLP pipeline: Raw Text -> Cleaning -> Stop Word Removal -> Lemmatization -> Word Tokenization.",
            "is_pipeline": True,
            "pipeline_stages": [
                {"stage": 1, "name": "Text Cleaning", "output": stage1_text},
                {"stage": 2, "name": "Stop Word Removal", "output": stage2_text},
                {"stage": 3, "name": "Lemmatization", "output": stage3_text},
                {"stage": 4, "name": "Final Tokenization", "output": final_tokens}
            ],
            "stats": {
                "char_count_orig": len(text),
                "char_count_proc": len(str(final_tokens)),
                "word_count_orig": len(re.findall(r'\w+', text)),
                "sentence_count": max(1, len(re.split(r'[.!?]+', text))),
                "tokens_count": len(final_tokens),
                "stopwords_removed": stage2_res["stats"].get("stopwords_removed", 0),
                "words_changed": stage3_res["stats"].get("words_changed", 0),
                "execution_time_ms": elapsed_ms
            },
            "python_code": self._generate_python_code("pipeline", "full_pipeline")
        }

    # ----------------------------------------------------
    # HELPER METADATA BUILDER & PYTHON CODE GENERATOR
    # ----------------------------------------------------
    def _build_result(self, original_text, tokens, technique, sub_type, explanation, start_time, processed_text=None):
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        
        orig_words = re.findall(r'\w+', original_text)
        orig_sentences = [s for s in re.split(r'[.!?]+', original_text) if s.strip()]
        
        if processed_text is None:
            if isinstance(tokens, list):
                processed_text = " ".join([str(t) for t in tokens])
            else:
                processed_text = str(tokens)

        # Word-only token filtering for accurate comparison
        orig_words_only = [w for w in re.findall(r'\w+', original_text)]
        proc_words_only = [str(t) for t in tokens if str(t).isalnum()] if isinstance(tokens, list) else [w for w in re.findall(r'\w+', str(processed_text))]

        # Token Frequency Analysis
        freq_counter = Counter([w.lower() for w in proc_words_only])
        top_freq = [{"token": k, "count": v} for k, v in freq_counter.most_common(8)]

        # Calculate word changes accurately
        words_changed = 0
        diff_list = []

        if isinstance(tokens, list) and len(tokens) > 0:
            for idx, orig_w in enumerate(orig_words_only):
                proc_w = proc_words_only[idx] if idx < len(proc_words_only) else ""
                is_changed = (orig_w.lower() != proc_w.lower()) and len(proc_w) > 0
                if is_changed:
                    words_changed += 1
                diff_list.append({
                    "original": orig_w,
                    "processed": proc_w if proc_w else orig_w,
                    "changed": is_changed
                })

        python_code = self._generate_python_code(technique, sub_type)

        return {
            "success": True,
            "original": original_text,
            "processed": processed_text,
            "output": tokens,
            "technique": technique,
            "sub_type": sub_type,
            "explanation": explanation,
            "diff": diff_list,
            "token_freq": top_freq,
            "python_code": python_code,
            "stats": {
                "char_count_orig": len(original_text),
                "char_count_proc": len(processed_text),
                "word_count_orig": len(orig_words),
                "sentence_count": max(1, len(orig_sentences)),
                "tokens_count": len(tokens) if isinstance(tokens, list) else len(proc_words_only),
                "stopwords_removed": 0,
                "words_changed": words_changed,
                "execution_time_ms": elapsed_ms
            }
        }

    def _generate_python_code(self, technique, sub_type):
        tech_lower = technique.lower()
        if "token" in tech_lower:
            if sub_type in ["word", "sentence"]:
                return f'''# SVCET NLP Lab - {sub_type.capitalize()} Tokenization
import nltk
from nltk.tokenize import { 'word_tokenize' if sub_type=='word' else 'sent_tokenize' }

text = "Natural Language Processing is amazing!"
tokens = { 'word_tokenize' if sub_type=='word' else 'sent_tokenize' }(text)
print("Tokens:", tokens)'''
            elif sub_type in ["bigram", "trigram", "ngram"]:
                n = 2 if sub_type=='bigram' else 3 if sub_type=='trigram' else 2
                return f'''# SVCET NLP Lab - N-gram Tokenization (N={n})
import re
text = "Natural Language Processing is amazing"
words = re.findall(r'\\w+', text)
ngrams = [" ".join(words[i:i+{n}]) for i in range(len(words)-{n}+1)]
print("N-grams:", ngrams)'''
            else:
                return f'''# SVCET NLP Lab - {sub_type.capitalize()} Tokenization
import re
text = "Natural Language Processing is amazing!"
tokens = re.findall(r'\\w+|[^\\w\\s]', text)
print("Tokens:", tokens)'''

        elif "stem" in tech_lower:
            return f'''# SVCET NLP Lab - Stemming ({sub_type.capitalize()})
import nltk
from nltk.stem import PorterStemmer, SnowballStemmer

stemmer = PorterStemmer() # or SnowballStemmer("english")
words = ["playing", "played", "plays", "player"]
stemmed = [stemmer.stem(w) for w in words]
print("Stemmed Words:", stemmed)'''

        elif "lemma" in tech_lower:
            return '''# SVCET NLP Lab - Lemmatization (WordNet & POS)
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

lemmatizer = WordNetLemmatizer()
words = ["children", "running", "playing", "better"]
lemmas = [lemmatizer.lemmatize(w, pos=wordnet.VERB) for w in words]
print("Lemmas:", lemmas)'''

        elif "stop" in tech_lower:
            return '''# SVCET NLP Lab - Stop Word Removal
import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
text = "This is a simple example of NLP"
filtered = [w for w in text.split() if w.lower() not in stop_words]
print("Filtered Text:", " ".join(filtered))'''

        elif "pipeline" in tech_lower:
            return '''# SVCET NLP Lab - Sequential Preprocessing Pipeline
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def nlp_pipeline(text):
    # 1. Clean Text
    text = re.sub(r'https?://\\S+|[^a-zA-Z0-9\\s]', '', text).lower().strip()
    # 2. Stop Words
    stops = set(stopwords.words('english'))
    words = [w for w in text.split() if w not in stops]
    # 3. Lemmatize & Tokenize
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(w) for w in words]
    return lemmas

print("Processed Pipeline Tokens:", nlp_pipeline("The 3 children are running!"))'''

        else:
            return '''# SVCET NLP Lab - Text Normalization
import re
text = "Hello World!!! Visit https://example.com"
clean_text = re.sub(r'https?://\\S+|[^a-zA-Z0-9\\s]', '', text).lower().strip()
print("Cleaned Text:", clean_text)'''


# Singleton processor instance
nlp_engine = NLPProcessor()
