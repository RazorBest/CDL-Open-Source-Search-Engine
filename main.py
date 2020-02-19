import cmd
import sys
import loader
import search


class Shell(cmd.Cmd):
    intro = "Welcome to the Open Source Search Engine. Type help or ? to list the commands.\n"
    prompt = '>>> '
    file = None
    wordsIndex = None

    def print_list_of_files(self, files):
        if len(files) == 0:
            print('Not found')
            return
        print('Found:')
        for file in files:
            print('    ' + file)

    def preloop(self):
        self.wordsIndex = loader.load_words_index('example_docs')

    def do_search(self, arg):
        files = search.search(arg, self.wordsIndex)
        self.print_list_of_files(files)

if __name__ == '__main__':
    Shell().cmdloop()