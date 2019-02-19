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


# sentences = [
#     "Dogs are awesome.",
#     "Some gorgeous creatures are felines.",
#     "Dolphins are swimming mammals.",
#     "Cats are beautiful animals.",
# ]
#
# focus_sentence = "Cats are beautiful animals."
#
# for sentence in sentences:
#     print("Similarity(\"%s\", \"%s\") = %s" % (focus_sentence, sentence, sentence_similarity(focus_sentence, sentence)))
#     print("Similarity(\"%s\", \"%s\") = %s" % (sentence, focus_sentence, sentence_similarity(sentence, focus_sentence)))

# Similarity("Cats are beautiful animals.", "Dogs are awesome.") = 0.511111111111
# Similarity("Dogs are awesome.", "Cats are beautiful animals.") = 0.666666666667

# Similarity("Cats are beautiful animals.", "Some gorgeous creatures are felines.") = 0.833333333333
# Similarity("Some gorgeous creatures are felines.", "Cats are beautiful animals.") = 0.833333333333

# Similarity("Cats are beautiful animals.", "Dolphins are swimming mammals.") = 0.483333333333
# Similarity("Dolphins are swimming mammals.", "Cats are beautiful animals.") = 0.4

# Similarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0
# Similarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0


# def symmetric_sentence_similarity(sentence1, sentence2):
#     """ compute the symmetric sentence similarity using Wordnet """
#     return (sentence_similarity(sentence1, sentence2) + sentence_similarity(sentence2, sentence1)) / 2
#
#
# print("\n\nSymmetric Similarity\n")
# for sentence in sentences:
#     print("SymmetricSimilarity(\"%s\", \"%s\") = %s" % (
#         focus_sentence, sentence, symmetric_sentence_similarity(focus_sentence, sentence)))
#     print("SymmetricSimilarity(\"%s\", \"%s\") = %s" % (
#         sentence, focus_sentence, symmetric_sentence_similarity(sentence, focus_sentence)))

# SymmetricSimilarity("Cats are beautiful animals.", "Dogs are awesome.") = 0.588888888889
# SymmetricSimilarity("Dogs are awesome.", "Cats are beautiful animals.") = 0.588888888889

# SymmetricSimilarity("Cats are beautiful animals.", "Some gorgeous creatures are felines.") = 0.833333333333
# SymmetricSimilarity("Some gorgeous creatures are felines.", "Cats are beautiful animals.") = 0.833333333333

# SymmetricSimilarity("Cats are beautiful animals.", "Dolphins are swimming mammals.") = 0.441666666667
# SymmetricSimilarity("Dolphins are swimming mammals.", "Cats are beautiful animals.") = 0.441666666667

# SymmetricSimilarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0
# SymmetricSimilarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0