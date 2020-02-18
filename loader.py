import os

def load_files(directory):
    files = os.listdir(directory)

    print(files)

if __name__ == '__main__':
    load_files('example_docs')