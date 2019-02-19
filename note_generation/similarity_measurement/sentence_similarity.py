from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn


def penn_to_wn(tag):
    # Convert between a Penn TreeBank tag to a simplified WordNet tag
    if tag.startswith('N'):
        return 'n'
    if tag.startswith('V'):
        return 'v'
    if tag.startswith('J'):
        return 'a'
    if tag.startswith('R'):
        return 'r'
    return None


def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


# Computing  sentence similarity using WordNet
def sentence_similarity(sentence1, sentence2):

    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0
    best_score = [0.0]

    # PATH SIMILARITY
    # for ss1 in synsets1:
    #     for ss2 in synsets2:
    #         best1_score = ss1.path_similarity(ss2)
    # if best1_score is not None:
    #     best_score.append(best1_score)
    # max1 = max(best_score)
    # if best_score is not None:
    #     score += max1
    # if max1 is not 0.0:
    #     count += 1
    # best_score = [0.0]
    # # print(score / count)

    # WUP SIMILARITY
    arr_simi_score = [0.0]
    similarity_score = 0.0
    for syn1 in synsets1:
        for syn2 in synsets2:
            similarity_score = syn1.wup_similarity(syn2)
    if similarity_score is not None:
        arr_simi_score.append(similarity_score)
    best = max(arr_simi_score)
    score += best
    count += 1

    return score


# Computing the symmetric sentence similarity using WordNet
def symmetric_sentence_similarity(sentence1, sentence2):
    return (sentence_similarity(sentence1, sentence2) + sentence_similarity(sentence2, sentence1)) / 2
