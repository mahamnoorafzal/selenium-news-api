
import re
from collections import Counter


def summarize_article(text, max_sentences=3):

    # Split article into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    sentences = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.split()) >= 8
    ]

    if not sentences:
        return "No sufficient text available for summarization."

    # Calculate word frequency
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    stop_words = {
        "the", "is", "are", "was", "were", "a", "an",
        "and", "or", "but", "in", "on", "at", "to",
        "of", "for", "with", "by", "from", "as",
        "that", "this", "it", "be", "has", "have",
        "had", "he", "she", "they", "their", "his",
        "her", "its", "will", "would", "could",
        "can", "said", "after", "before", "about"
    }

    important_words = [
        word for word in words
        if word not in stop_words and len(word) > 2
    ]

    frequency = Counter(important_words)

    # Score each sentence
    sentence_scores = {}

    for index, sentence in enumerate(sentences):
        sentence_words = re.findall(
            r'\b[a-zA-Z]+\b',
            sentence.lower()
        )

        score = sum(
            frequency[word]
            for word in sentence_words
            if word not in stop_words
        )

        sentence_scores[index] = score

    # Select the highest scoring sentences
    selected = sorted(
        sentence_scores,
        key=sentence_scores.get,
        reverse=True
    )[:max_sentences]

    # Maintain original article order
    selected.sort()

    summary = " ".join(
        sentences[index] for index in selected
    )

    return summary
