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
        # TODO validate the query
        files = []
        for directory, wordsIndex in self.dirIndex.items():
            files.extend(search.search(arg, wordsIndex))

        self.print_list_of_files(files)

    def do_load(self, arg):
        """load [directory]
            Add a new directory to the search index
        """
        if not os.path.isdir(arg):
            print('"' + arg + '" is not a directory os does not exist')
            return

        dir_id = loader.get_path_id(arg)
        wordsIndex = loader.load_words_index_from_directory(arg)
        self.dirIndex[dir_id] = wordsIndex

    def do_remove(self, arg):
        """remove [directory]
            Remove a directory from the search index
        """
        dir_id = loader.get_path_id(arg)
        if not dir_id in self.dirIndex:
            print('"' + arg + '" is not a loaded directory. Type list to see loaded directories')
            return

        del self.dirIndex[dir_id]
        os.remove(loader.DATA_DIRECTORY + dir_id)
        print(arg + ' deleted')

    def do_list(self, arg):
        """List the loaded directories from the search index
        """
        for wordsIndex in self.dirIndex.values():
            print(wordsIndex.directoryPath)

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
