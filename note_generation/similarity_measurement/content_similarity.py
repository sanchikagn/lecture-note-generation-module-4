from .sentence_similarity import sentence_similarity
import pandas as pd


def word_net_similarity(sentences, focus_sentence):
    # Sentences are from lecture transcript
    # Focus_sentences are from ontology
    sent_freq = []
    lecture_text = pd.DataFrame(columns=['sentence', 'freq', 'label'])
    for sentence in sentences:
        for sent in focus_sentence:
            similarity_sent = sentence_similarity(sent, sentence)
            sent_freq.append(similarity_sent)
            if similarity_sent < 0.3:
                lecture_text = lecture_text.append({'sentence': sentence, 'sent': sent, 'freq': similarity_sent, 'label': 'off'},
                                                   ignore_index=True)
            else:
                lecture_text = lecture_text.append({'sentence': sentence, 'sent': sent, 'freq': similarity_sent, 'label': 'on'},
                                                   ignore_index=True)
    return lecture_text


# def word_net_similarity(topic, sentences, focus_sentence, images):
#     # Sentences are from lecture transcript
#     # Focus_sentences are from ontology
#     sent_freq = []
#     lecture_text = pd.DataFrame(columns=['sentence', 'freq', 'label', 'topic', 'images'])
#     for sentence in sentences:
#         for sent in focus_sentence:
#             similarity_sent = sentence_similarity(sent, sentence)
#             sent_freq.append(similarity_sent)
#             if similarity_sent < 0.3:
#                 lecture_text = lecture_text.append({'sentence': sentence, 'freq': similarity_sent, 'label': 'off',
#                                                     'topic': topic, 'images': images},ignore_index=True)
#             else:
#                 lecture_text = lecture_text.append({'sentence': sentence, 'freq': similarity_sent, 'label': 'on',
#                                                     'topic': topic, 'images': images},ignore_index=True)
#     # print(lecture_text)
#     return lecture_text
