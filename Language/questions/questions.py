import nltk
nltk.download('stopwords')
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
    files_dict = {}
    for file in os.listdir(directory):
        #print(file)
        files_dict[file] = open(os.path.join(directory,file), "r", encoding = sys.getdefaultencoding(), closefd = True, opener = None).read()
        #print(open(os.path.join(directory,file)).read())
    #print(files_dict)
    return files_dict



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    doc = nltk.tokenize.word_tokenize(document)
    tokens = []
    for word in doc:
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            tokens.append(word)    
    return tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    doc_count = {}
    idfs = {}
    uwords = set()
    for doc in documents:
        for word in documents[doc]:
            uwords.add(word)
    for word in uwords:
        doc_count[word] = 0
        idfs[word] = 0
    for doc in documents:
        for word in uwords:
            if word in documents[doc]:
                doc_count[word] += 1
    for word in idfs:
        idfs[word] = math.log(len(documents)/doc_count[word])
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    best_file_list = []
    file_assignments = {}
    for file in files:
        sum = 0
        for word in query:
            count = 0
            for w in files[file]:
                if word == w:
                    count += 1
            tfidf = idfs[word] * count
            sum += tfidf
        file_assignments[file] = sum
    for i in range(n):
        best_file = max(file_assignments, key = file_assignments.get)
        best_file_list.append(best_file) 
        del file_assignments[best_file]
    return best_file_list
    



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # print(query)
    # sum1 = 0
    # for word in query:
    #     print("sum: ", sum1)
    #     sum1 += idfs[word]
    #     print(word, idfs[word])
    # print(sum1)
    best_sentence_list = []
    sentence_assignments = {}
    for sentence in sentences:
        # if sentence == 'Python 3.0 was released on 3 December 2008.' or sentence == 'Python 3.0, released in 2008, was a major revision of the language that is not completely backward-compatible, and much Python 2 code does not run unmodified on Python 3.':
        #     print(sentences[sentence])
        #     sum = 0
        #     for word in query:
        #         if word in sentences[sentence]:
        #             print(word, idfs[word])
        #             sum += idfs[word]
        #     sentence_assignments[sentence] = sum
        sum = 0
        for word in query:
            if word in sentences[sentence]:
                sum += idfs[word]
        sentence_assignments[sentence] = sum
    storage = {}
    for p in sentence_assignments:
        storage[p] = sentence_assignments[p]
    #print(sentence_assignments)
    for i in range(n):
        best_sentence = max(sentence_assignments, key = sentence_assignments.get)
        other_sentences = []
        for p in sentence_assignments:
            if p != best_sentence and sentence_assignments[p] == sentence_assignments[best_sentence]:
                other_sentences.append(p)
        other_sentences.append(best_sentence)
        for i in range(len(other_sentences)-1):
            if needs_swap(query,sentences,storage,other_sentences[i],other_sentences[i + 1]):
                temp = other_sentences[i]
                other_sentences[i] = best_sentence_list[i + 1]
                other_sentences[i + 1] = temp
        best_sentence_list.append(other_sentences[0]) 
        del sentence_assignments[best_sentence]
    print(storage)
    # print(n)
    # for i in range(n-1):
    #     # count1, count2 = needs_swap(query,sentences,storage,best_sentence_list[i],best_sentence_list[i + 1])
    #     if needs_swap(query,sentences,storage,best_sentence_list[i],best_sentence_list[i + 1]):
    #         temp = best_sentence_list[i]
    #         best_sentence_list[i] = best_sentence_list[i + 1]
    #         best_sentence_list[i + 1] = temp

    return best_sentence_list
def needs_swap(query,sentences,sentence_assignments,sentence1,sentence2):
    if sentence_assignments[sentence1] == sentence_assignments[sentence2]:
        count1 = 0.0
        for word in sentences[sentence1]:
            if word in query:
                count1 += 1
        count2 = 0.0
        for word in sentences[sentence2]:
            if word in query:
                count2 += 1
        count1 /= len(sentences[sentence1])
        count2 /= len(sentences[sentence2])
        #return count1, count2
        if count2 > count1:
            return True
        else:
            return False


if __name__ == "__main__":
    main()
