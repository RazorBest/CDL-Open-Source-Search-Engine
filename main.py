import cmd
import sys
import loader
import search


class Shell(cmd.Cmd):
    intro = "Welcome to the Open Source Search Engine. Type help or ? to list the commands.\n"
    prompt = '>>> '
    file = None
    dirIndex = None
    wordsIndex = None

    def preloop(self):
        # dirIndex is a list of loader.DirectoryInvertedIndex objects
        self.dirIndex = loader.load_words_index()

    def do_search(self, arg):
        files = []
        for directory, wordsIndex in self.dirIndex.items():
            files.extend(search.search(arg, wordsIndex))

        self.print_list_of_files(files)

    def do_load(self, arg):
        wordsIndex = loader.load_words_index_from_directory(arg)
        self.dirIndex[arg] = wordsIndex

    def do_remove(self, arg):
        del self.dirIndex[arg]
        print(arg + ' deleted')

    def do_list(self, arg):
        for directory in self.dirIndex:
            print(directory)

    def do_exit(self, arg):
        print('Exitting the shell...')
        return True

    def do_quit(self, arg):
        self.exit(arg)

    def print_list_of_files(self, files):
        if len(files) == 0:
            print('Not found')
            return
        print('Found:')
        for file in files:
            print('    ' + file)


if __name__ == '__main__':
    Shell().cmdloop()
