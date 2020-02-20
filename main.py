import cmd
import sys
import loader
import search
import os

class Shell(cmd.Cmd):
    intro = "Welcome to the Open Source Search Engine. Type help or ? to list the commands.\nType search [query] to query the documents\n"
    prompt = '>>> '
    file = None
    dirIndex = None
    wordsIndex = None

    def preloop(self):
        # dirIndex is a list of loader.DirectoryInvertedIndex objects
        self.dirIndex = loader.load_words_index()

    def do_search(self, arg):
        """search [query]
            Search in the loaded directorires using the query
        """
        files = []
        for directory, wordsIndex in self.dirIndex.items():
            files.extend(search.search(arg, wordsIndex))

        self.print_list_of_files(files)

    def do_load(self, arg):
        """load [directory]
            Add a new directory to the search index
        """
        wordsIndex = loader.load_words_index_from_directory(arg)
        self.dirIndex[arg] = wordsIndex

    def do_remove(self, arg):
        """remove [directory]
            Remove a directory from the search index
        """
        del self.dirIndex[arg]
        os.remove(loader.DATA_DIRECTORY + '/' + arg)
        print(arg + ' deleted')

    def do_list(self, arg):
        """List the loaded directories from the search index
        """
        for directory in self.dirIndex:
            print(directory)

    def do_exit(self, arg):
        """Exit the shell
        """
        print('Exitting the shell...')
        return True

    def do_quit(self, arg):
        """Exit the shell
        """
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
