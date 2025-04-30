import streamlit as st
from flashcard import generate_flashcards, get_flashcard_word_count
from image_processing import extract_text
from text_to_speech import text_to_speech
import random

# Page configuration
st.set_page_config(
    page_title="Smart Flashcard Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'flashcards' not in st.session_state:
    st.session_state.flashcards = {}
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'cards_generated' not in st.session_state:
    st.session_state.cards_generated = 0
if 'texts_processed' not in st.session_state:
    st.session_state.texts_processed = 0
if 'last_shuffle_state' not in st.session_state:
    st.session_state.last_shuffle_state = False
if 'shuffled_keys' not in st.session_state:
    st.session_state.shuffled_keys = []
if 'input_method' not in st.session_state:
    st.session_state.input_method = "Text"
if 'text_word_count' not in st.session_state:
    st.session_state.text_word_count = 0
if 'flashcard_word_count' not in st.session_state:
    st.session_state.flashcard_word_count = 0

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Controls")

    # Stats display
    st.markdown("### 📊 Session Stats")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="stat-item">
                <div class="stat-value">{st.session_state.cards_generated}</div>
                <div class="stat-label">Cards Generated</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="stat-item">
                <div class="stat-value">{st.session_state.texts_processed}</div>
                <div class="stat-label">Texts Processed</div>
            </div>
        """, unsafe_allow_html=True)

    # Word count stats
    st.markdown(f"""
        <div class="stat-item">
            <div class="stat-value">{st.session_state.text_word_count}</div>
            <div class="stat-label">Words in Text</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="stat-item">
            <div class="stat-value">{st.session_state.flashcard_word_count}</div>
            <div class="stat-label">Words in Flashcards</div>
        </div>
    """, unsafe_allow_html=True)

    # Options
    st.markdown("### 🔧 Options")
    shuffle_cards = st.checkbox("Shuffle Cards", value=False)

# Main input form
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="input-method-title">Choose Your Input Method</div>', unsafe_allow_html=True)

    col_text, col_image = st.columns(2)
    with col_text:
        if st.button("Text", key="text_btn", use_container_width=True):
            st.session_state.input_method = "Text"
            st.rerun()
    with col_image:
        if st.button("Image", key="image_btn", use_container_width=True):
            st.session_state.input_method = "Image"
            st.rerun()

    with st.form(key="input_form"):
        if st.session_state.input_method == "Text":
            text_input = st.text_area("Enter your text to generate flashcards:", height=300)
            submit_button = st.form_submit_button("Generate Flashcards", use_container_width=True)

            if submit_button:
                if text_input.strip():
                    with st.spinner("Generating intelligent flashcards..."):
                        flashcards = generate_flashcards(text_input)
                        if flashcards is not None:
                            st.session_state.flashcards = flashcards
                            st.session_state.current_index = 0
                            st.session_state.cards_generated += len(flashcards)
                            st.session_state.texts_processed += 1
                            st.session_state.text_word_count = len(text_input.split())
                            st.session_state.flashcard_word_count = get_flashcard_word_count(flashcards)
                        else:
                            st.warning("Flashcard generation failed.")
                else:
                    st.warning("Please enter some text!")

        elif st.session_state.input_method == "Image":
            uploaded_file = st.file_uploader("Upload an image containing text", type=["png", "jpg", "jpeg"])
            submit_button = st.form_submit_button("Extract & Generate Flashcards", use_container_width=True)

            if submit_button:
                if uploaded_file is not None:
                    with st.spinner("Processing image and generating flashcards..."):
                        image_path = f"temp_{uploaded_file.name}"
                        with open(image_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        extracted_text = extract_text(image_path)
                        flashcards = generate_flashcards(extracted_text)
                        if flashcards is not None:
                            st.session_state.flashcards = flashcards
                            st.session_state.current_index = 0
                            st.session_state.cards_generated += len(flashcards)
                            st.session_state.texts_processed += 1
                            st.session_state.text_word_count = len(extracted_text.split())
                            st.session_state.flashcard_word_count = get_flashcard_word_count(flashcards)
                        else:
                            st.warning("Flashcard generation failed.")
                else:
                    st.warning("Please upload an image!")

with col2:
    if st.session_state.flashcards and len(st.session_state.flashcards) > 0:
        flashcards = st.session_state.flashcards
        current_index = st.session_state.current_index

        if shuffle_cards and st.session_state.last_shuffle_state != shuffle_cards:
            keys = list(flashcards.keys())
            random.shuffle(keys)
            st.session_state.shuffled_keys = keys

        st.session_state.last_shuffle_state = shuffle_cards

        keys = st.session_state.shuffled_keys if shuffle_cards and st.session_state.shuffled_keys else list(flashcards.keys())
        values = [flashcards[k] for k in keys]

        progress = (current_index + 1) / len(flashcards) if flashcards else 0
        st.markdown(f"""
            <div class="progress-container">
                <div style="height: 100%; width: {progress * 100}%; background-color: #2b6cb0;"></div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="flashcard-container">', unsafe_allow_html=True)

        current_index = max(0, min(current_index, len(values) - 1))

        st.markdown(f"""
            <div class="flashcard">
                <div class="card-content">{values[current_index]}</div>
                <div class="card-counter">{current_index + 1}/{len(flashcards)}</div>
            </div>
        """, unsafe_allow_html=True)

        col_left, col_middle, col_right = st.columns([1, 2, 1])
        with col_left:
            if st.button("⬅️ Previous", key="prev_btn", disabled=current_index == 0):
                st.session_state.current_index -= 1
                st.rerun()

        with col_middle:
            if st.button("🔊 Read Aloud", key="audio_btn"):
                with st.spinner("Converting to speech..."):
                    text_to_speech(values[current_index])
                    st.success("Audio saved as 'flashcard.mp3'")

        with col_right:
            if st.button("Next ➡️", key="next_btn", disabled=current_index == len(flashcards) - 1):
                st.session_state.current_index += 1
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("Show Key Phrase"):
            st.write(f"**Key Phrase:** {keys[current_index]}")
    else:
        st.markdown("""
            <div class="empty-state">
                <h2 class="empty-state-title">No Flashcards Yet</h2>
                <p class="empty-state-text">
                    Enter your study material or upload an image on the left to generate AI-powered flashcards.
                </p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        Smart Flashcard Generator • Powered by AI  <br>
        © Chinmay Keripale & Asim Kazi 
    </div>
""", unsafe_allow_html=True)
