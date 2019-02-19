from .sentence_similarity import symmetric_sentence_similarity
import pandas as pd


def word_net_similarity(sentences, focus_sentence):
    # Sentences are from lecture transcript
    # Focus_sentences are from ontology
    sent_freq = []
    lecture_text = pd.DataFrame(columns=['sentence', 'freq', 'label'])
    for sentence in sentences:
        freq = 0.0
        for sent in focus_sentence:
            similarity_sent = symmetric_sentence_similarity(sent, sentence)
            sent_freq.append(similarity_sent)

        # Get weighted similarity
        for item in sent_freq:
            freq = freq + item
        sentence_freq = freq/(len(sent_freq))
        if sentence_freq < 0.3:
            lecture_text = lecture_text.append(
                {'sentence': sentence, 'freq': sentence_freq, 'label': 'off'},
                ignore_index=True)
        else:
            lecture_text = lecture_text.append(
                {'sentence': sentence, 'freq': sentence_freq, 'label': 'on'},
                ignore_index=True)
    return lecture_text
