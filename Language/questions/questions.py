import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    nameToContent = {}
    for file in os.listdir(directory):
        nameToContent[file] = open(os.path.join(directory,file)).read()
    return nameToContent


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    unfiltered = nltk.tokenize.word_tokenize(document.lower())
    filtered = []
    for token in unfiltered:
        if token not in string.punctuation and token not in nltk.corpus.stopwords.words("english"):
            filtered.append(token)
    return filtered



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    word_to_idf = {}
    #collect number of docs for each word
    for doc in documents:
        for word in set(documents[doc]):
            if word in word_to_idf:
                word_to_idf[word] += 1
            else:
                word_to_idf[word] = 1
    for word in word_to_idf:
        num_appearances = word_to_idf[word]
        word_to_idf[word] = math.log(len(documents) / num_appearances)
    return word_to_idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    #dictionary matching files to their sums
    file_to_sum = {}
    for file in files:
        sum = 0
        for word in query:
            if word in files[file]:
                freq = 0
                for word2 in files[file]:
                    if word2 == word:
                        freq += 1
                sum += freq * idfs[word]
        file_to_sum[file] = sum
    #list of files ranked with top ranked in first positions
    top_ranked_files = sorted(file_to_sum, file_to_sum.get, reverse = True)
    return top_ranked_files[:n]




def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_to_sum = {}
    for sentence in sentences:
        sum = 0
        for word in query:
            if word in sentences[sentence]:
                sum += idfs[word]
        sentence_to_sum[sentence] = sum
    top_ranked_sentences = sorted(sentence_to_sum, sentence_to_sum.get, reverse = True)
    for i in range(len(top_ranked_sentences) - 1):
        sentence1 = top_ranked_sentences[i]
        sentence2 = top_ranked_sentences[i + 1]
        if sentence_to_sum[sentence1] == sentence_to_sum[sentence2]:
            q_d1 = 0
            for word in sentence1:
                if word in query:
                    q_d1 += 1
            q_d1 /= len(sentence1)
            q_d2 = 0
            for word in sentence2:
                if word in query:
                    q_d2 += 1
            q_d2 /= len(sentence2)
            if q_d2 > q_d1:
                temp = top_ranked_sentences[i]
                top_ranked_sentences[i] = top_ranked_sentences[i + 1]
                top_ranked_sentences[i + 1] = temp
    return top_ranked_sentences[:n]


if __name__ == "__main__":
    main()
