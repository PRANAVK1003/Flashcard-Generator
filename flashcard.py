import spacy
import numpy as np
import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Initialize the summarization pipeline
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
def load_embedder():
    return SentenceTransformer('all-MiniLM-L6-v2')

def preprocess_text(text):
    """Splits text into sentences while maintaining structure and meaning."""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    return sentences

def determine_flashcard_count(text):
    """Determines the number of flashcards based on text length."""
    word_count = len(text.split())
    if word_count < 100:
        return 3
    elif 100 <= word_count < 300:
        return 5
    elif 300 <= word_count < 600:
        return 7
    else:
        return 10

def generate_flashcards(text):
    num_flashcards = determine_flashcard_count(text)
    sentences = preprocess_text(text)

    if not sentences:
        return {}

    model = load_embedder()
    embeddings = model.encode(sentences)
    similarity_matrix = cosine_similarity(embeddings)

    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)

    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    selected = []
    used_phrases = set()

    for _, sentence in ranked_sentences:
        if len(selected) >= num_flashcards:
            break
        cleaned = sentence.strip()
        if cleaned and cleaned not in used_phrases:
            trimmed = '. '.join(cleaned.split('. ')[:3]).strip()
            if not trimmed.endswith('.'):
                trimmed += '.'
            selected.append(trimmed)
            used_phrases.add(trimmed)

    # Use selected sentences directly (no summarization)
    summarized_flashcards = selected
    flashcards = {f"Point {i+1}": point for i, point in enumerate(summarized_flashcards)}
    return flashcards


def get_flashcard_word_count(flashcards):
    """Counts the total number of words in all flashcards."""
    return sum(len(card.split()) for card in flashcards.values())
