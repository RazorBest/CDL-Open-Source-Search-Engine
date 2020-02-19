import os
import re
from bitstring import BitArray
import pickle

DATA_DIRECTORY = '.data/'
# Words that are too common and are ignored
STOPWORDS = ['a', 'and', 'every', 'for', 'from', 'in', 'is', 'it',
             'not', 'on', 'one', 'the', 'to']

class DirectoryInvertedIndex:
    def __init__(self, filenames):
        self.wordsIndex = {}
        self.filenames = tuple(filenames)
        self.files_count = len(filenames)
    
    def __iter__(self):
        return iter(self.wordsIndex)

    def __getitem__(self, key):
        return self.wordsIndex[key]

    def __setitem__(self, key, item):
        self.wordsIndex[key] = item

    def init_item(self, key):
        self.wordsIndex[key] = BitArray(self.files_count)

def save_data(data, dirname):
    path = DATA_DIRECTORY + dirname
    if not os.path.isdir(DATA_DIRECTORY):
        os.mkdir(DATA_DIRECTORY)
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def get_sorted_filenames(directory):
    files = os.listdir(directory)
    files.sort()
    return files

def load_files(directory):
    """Read the files from directory; index the words in 
        files using an Inverted Index data structure and 
        return it.
    """
    # The data structure that keeps our words
   

    files = get_sorted_filenames(directory)
    wordsIndex = DirectoryInvertedIndex(files)

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
                    wordsIndex.init_item(word)

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
