import os
import re
from bitstring import BitArray
import pickle

DATA_DIRECTORY = '.data/'
# Words that are too common and are ignored
STOPWORDS = ['a', 'and', 'every', 'for', 'from', 'in', 'is', 'it',
             'not', 'on', 'one', 'the', 'to']


def save_data(data, dirname):
    path = DATA_DIRECTORY + dirname
    if not os.path.isdir(DATA_DIRECTORY):
        os.mkdir(DATA_DIRECTORY)
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def load_files(directory):
    """Read the files from directory; index the words in 
        files using an Inverted Index data structure and 
        return it.
    """
    # The data structure that keeps our words
    wordsIndex = {}

    files = os.listdir(directory)
    files.sort()
    files_count = len(files)

    # Read every file in the files list
    for file_index, filename in enumerate(files):
        path = directory + '/' + filename
        with open(path, "r") as f:
            text = f.read().lower()
            # Split the text in words, ingoring whitespaces and dellimiters
            words = re.findall(r"[\w']+", text)

            # Update the index for every word
            for word in words:
                # Ignore the useless words
                if word in STOPWORDS:
                    continue

                if not word in wordsIndex:
                    # Initialise the apparition array for the
                    wordsIndex[word] = BitArray(files_count)

                wordsIndex[word][file_index] = 1

    return wordsIndex


def load_words_index(directory):
    """Returns the Inverted Index from the files of a directory"""
    path = DATA_DIRECTORY + directory
    # If the directory wasn't indexed before
    if not os.path.isfile(path):
        wordsIndex = load_files(directory)
        save_data(wordsIndex, directory)

        return wordsIndex
    
    with open(path, 'rb') as f:
        wordsIndex = pickle.load(f)

        return wordsIndex


if __name__ == '__main__':
    wordsIndex = load_words_index('example_docs')

    print('wordsIndex has ' + str(len(wordsIndex)) + ' words')
