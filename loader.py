import os
import re
from bitstring import BitArray
import pickle

# Words that are too common and are ignored
STOPWORDS = ['a', 'and', 'every', 'for', 'from', 'in', 'is', 'it',
             'not', 'on', 'one', 'the', 'to']


def save_data(data, dirname):
    path = '.data/' + dirname
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def load_files(directory):
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


if __name__ == '__main__':
    wordsIndex = load_files('example_docs')

    print('wordsIndex has ' + str(len(wordsIndex)) + ' words')
