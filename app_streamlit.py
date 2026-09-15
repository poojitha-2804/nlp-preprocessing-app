"""
SVCET Chittoor - NLP Preprocessing Streamlit Application
Developed by V. Poojitha & R. Jai Sree Ram, CSE (AI & ML)
"""

import streamlit as st
import pandas as pd
import json
import re
from utils.nlp_processor import nlp_engine

# Page Configuration
st.set_page_config(
    page_title="SVCET NLP Preprocessing Techniques",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Mint Green & Light Theme)
st.markdown("""
<style>
    .main {
        background-color: #F4FBF7;
    }
    .stButton>button {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    .header-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #10B981;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-card">
    <h1 style="color: #0D3B11; margin-bottom: 5px;">🌿 SVCET CHITTOOR</h1>
    <h3 style="color: #10B981; margin-top: 0;">NLP DATA PREPROCESSING TECHNIQUES</h3>
    <p style="color: #4B5563;">Sri Venkateswara College of Engineering & Technology (Autonomous) | Developed by V. Poojitha & R. Jai Sree Ram, CSE (AI & ML)</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
nav_choice = st.sidebar.radio("Select View:", [
    "🚀 Guided Exploration Stepper",
    "🧪 NLP Workbench Lab",
    "⚔️ Algorithm Battle Arena",
    "📚 Technique Reference"
])

# ----------------------------------------------------
# VIEW 1: GUIDED EXPLORATION STEPPER
# ----------------------------------------------------
if nav_choice == "🚀 Guided Exploration Stepper":
    st.header("🚀 6-Step NLP Preprocessing Pipeline Stepper")
    st.caption("Step through the text transformation pipeline live.")

    sample_text = st.text_area("Input Text:", value="The 3 happy children were running fast to https://svcet.in! 😊", height=100)
    
    step = st.slider("Select Milestone Step:", 1, 6, 1)

    if step == 1:
        st.subheader("Step 1: Raw Unstructured Intake")
        st.info(sample_text)
        st.caption("Raw uncleaned text containing numbers, URLs, emojis, and punctuation.")
    elif step == 2:
        st.subheader("Step 2: Lowercasing & Cleaning")
        cleaned = sample_text.toLowerCase() if hasattr(sample_text, 'toLowerCase') else sample_text.lower()
        cleaned = re.sub(r'https?://\S+|www\.\S+', '', cleaned)
        cleaned = re.sub(r'[^\w\s]', ' ', cleaned)
        st.success(cleaned)
        st.caption("Lowercased and stripped of URLs, emojis, and special characters.")
    elif step == 3:
        st.subheader("Step 3: Stop Words Removal")
        stops = {'the', 'a', 'an', 'were', 'to', 'was', 'is', 'are', 'in', 'at'}
        words = [w for w in sample_text.lower().split() if w not in stops]
        st.success(" ".join(words))
        st.caption("High-frequency structural words removed.")
    elif step == 4:
        st.subheader("Step 4: Stemming & Lemmatization")
        res = nlp_engine.stem(sample_text, algorithm='porter')
        st.code(res.get('processed_text', ''))
        st.caption("Suffixed word variations reduced to root forms.")
    elif step == 5:
        st.subheader("Step 5: Token Segmentation")
        tokens = nlp_engine.tokenize(sample_text, token_type='word')
        st.json(tokens.get('tokens', []))
        st.caption("Text split into discrete token elements array.")
    elif step == 6:
        st.subheader("Step 6: Numerical Vector IDs")
        tokens = nlp_engine.tokenize(sample_text, token_type='word').get('tokens', [])
        ids = [100 + idx * 5 for idx in range(len(tokens))]
        st.write(ids)
        st.caption("Tokens converted into numerical embedding IDs for machine learning models.")

# ----------------------------------------------------
# VIEW 2: NLP WORKBENCH LAB
# ----------------------------------------------------
elif nav_choice == "🧪 NLP Workbench Lab":
    st.header("🧪 NLP Workbench Lab")
    user_input = st.text_area("Enter Custom Text for Preprocessing:", "SVCET Chittoor students love studying Natural Language Processing algorithms!", height=120)
    
    col1, col2 = st.columns(2)
    with col1:
        technique = st.selectbox("Select Technique:", ["Tokenization", "Stemming", "Lemmatization", "Stop Word Removal", "Text Cleaning", "POS Tagging"])
    with col2:
        if technique == "Tokenization":
            option = st.selectbox("Algorithm:", ["word", "wordpiece", "regex", "n_gram", "whitespace", "character"])
        elif technique == "Stemming":
            option = st.selectbox("Algorithm:", ["porter", "snowball", "lancaster", "rule_based", "lovins"])
        elif technique == "Lemmatization":
            option = st.selectbox("Algorithm:", ["wordnet", "pos_based", "context_aware", "dictionary", "rule_based"])
        elif technique == "Stop Word Removal":
            option = st.selectbox("Algorithm:", ["standard", "aggressive", "domain_nlp", "frequency", "custom"])
        else:
            option = st.selectbox("Algorithm:", ["full_pipeline", "lowercase", "remove_urls", "remove_html", "remove_numbers", "remove_punctuation"])

    if st.button("⚡ Process Text"):
        if technique == "Tokenization":
            res = nlp_engine.tokenize(user_input, token_type=option)
            st.success("Tokens Extracted:")
            st.write(res.get('tokens', []))
        elif technique == "Stemming":
            res = nlp_engine.stem(user_input, algorithm=option)
            st.success(res.get('processed_text', ''))
        elif technique == "Lemmatization":
            res = nlp_engine.lemmatize(user_input, method=option)
            st.success(res.get('processed_text', ''))
        elif technique == "Stop Word Removal":
            res = nlp_engine.remove_stopwords(user_input, method=option)
            st.success(res.get('processed_text', ''))
        elif technique == "Text Cleaning":
            res = nlp_engine.clean_text(user_input, method=option)
            st.success(res.get('processed_text', ''))

# ----------------------------------------------------
# VIEW 3: ALGORITHM BATTLE ARENA
# ----------------------------------------------------
elif nav_choice == "⚔️ Algorithm Battle Arena":
    st.header("⚔️ Side-by-Side Algorithm Battle Arena")
    battle_text = st.text_input("Enter text to compare algorithms:", "this is a book. The children were running fast!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("WordNet Lemmatization")
        st.code(nlp_engine.lemmatize(battle_text, method='wordnet').get('processed_text', ''))
        st.caption("Standard NLTK WordNet dictionary lookup.")
    with col2:
        st.subheader("POS-Based Lemmatization")
        st.code(nlp_engine.lemmatize(battle_text, method='pos_based').get('processed_text', ''))
        st.caption("Morphological POS tagging tagger ('were' -> 'be', 'running' -> 'run').")

# ----------------------------------------------------
# VIEW 4: REFERENCE
# ----------------------------------------------------
elif nav_choice == "📚 Technique Reference":
    st.header("📚 NLP Preprocessing Techniques Summary")
    df = pd.DataFrame([
        {"Technique": "Tokenization", "Algorithms": "11 (Word, WordPiece, BPE, N-Gram, Regex...)", "Purpose": "Splits text into atomic language units."},
        {"Technique": "Stemming", "Algorithms": "5 (Porter, Snowball, Lancaster, Lovins...)", "Purpose": "Strips word suffixes to base crude roots."},
        {"Technique": "Lemmatization", "Algorithms": "5 (WordNet, POS-Based, Context-Aware, Dict, Rule)", "Purpose": "Maps inflected words to valid dictionary lemmas."},
        {"Technique": "Stopwords Removal", "Algorithms": "5 (Standard, Aggressive, Frequency...)", "Purpose": "Filters non-informative structural words."},
        {"Technique": "Text Cleaning", "Algorithms": "10 (Lowercase, URL, HTML, Emojis...)", "Purpose": "Strips noise before feature extraction."}
    ])
    st.table(df)

# Footer
st.markdown("---")
st.caption("© 2026 SVCET NLP Preprocessing Platform . Developed by V. Poojitha & R. Jai Sree Ram, CSE (AI & ML)")
