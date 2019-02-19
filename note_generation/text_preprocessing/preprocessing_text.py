import nltk
import pandas as pd
import string
import re

from nltk import WordNetLemmatizer
stopwords = nltk.corpus.stopwords.words('english')
word_lemmatizer = WordNetLemmatizer()


# Removing punctuation
def removing_punctuation(content):
    punctuation_removed_content = "".join([word for word in content if word not in string.punctuation])
    return punctuation_removed_content


# Senetence tokenizing
def tokenize_into_sentences(content):
    sent_text = nltk.sent_tokenize(content)
    return sent_text


# Converting to lowercase and word tokenizing
def tokenize_into_words(content):
    tokens_lowercase = " ".join(x.lower() for x in content.split())
    tokens = re.split('\W+', tokens_lowercase)
    return tokens


# Removing stop English words
def remove_stopwords(tokenized_word_list):
    text = [word for word in tokenized_word_list if word not in stopwords]
    return text


# Lemmatizing
def lemmatization(tokenized_words):
    lemmatized_text = [word_lemmatizer.lemmatize(word)for word in tokenized_words]
    return ' '.join(lemmatized_text)


# Applying pre-processing to topics
def preprocessing_topics(lecture_content):
    print('Pre-processing Topics')
    # df for text analyzing
    lecture_text = pd.DataFrame(columns=['start', 'end', 'topic', 'content', 'images'])
    lecture_text['start'] = lecture_content['start']
    lecture_text['end'] = lecture_content['end']
    lecture_text['images'] = lecture_content['images']

    lecture_text['topic'] = lecture_content['topic'].apply(lambda topic: removing_punctuation(topic))
    lecture_text['topic'] = lecture_text['topic'].apply(lambda topic: tokenize_into_words(topic))
    lecture_text['topic'] = lecture_text['topic'].apply(lambda topic: remove_stopwords(topic))
    lecture_text['topic'] = lecture_text['topic'].apply(lambda topic: lemmatization(topic))
    return lecture_text


# Applying pre-processing to content
def preprocessing_content(lecture_content):
    print('Pre-processing Content')
    lecture_text = pd.DataFrame(columns=['start', 'end', 'topic', 'content', 'images'])
    lecture_text['start'] = lecture_content['start']
    lecture_text['end'] = lecture_content['end']
    lecture_text['images'] = lecture_content['images']
    lecture_text['content'] = lecture_content['content']
    lecture_text['topic'] = lecture_content['topic']

    lecture_text['content'] = lecture_text['content'].apply(lambda content: tokenize_into_sentences(content))
    return lecture_text


# Applying pre-processing to topic
def preprocessing_topic(topic):
    print('Pre-processing Topics')
    topic = removing_punctuation(topic)
    keywords = tokenize_into_words(topic)
    keywords = remove_stopwords(keywords)
    keywords = lemmatization(keywords)
    return keywords


# Applying pre-processing to content
def preprocessing_acontent(lecture_content):
    print('Pre-processing Content')
    lecture_content = tokenize_into_sentences(lecture_content)
    return lecture_content
