import os

def load_files(directory):
    files = os.listdir(directory)

    for filename in files:
        path = directory + '/' + filename
        with open(path, "r") as f:
            text = f.read()

if __name__ == '__main__':
    load_files('example_docs')