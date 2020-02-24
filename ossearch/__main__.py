import sys
from . import shell
from . import GUI

def main():
    args = sys.argv[1:]
    
    if len(args) >= 1 and args[0] == 'shell':
        shell.main()
        return

    GUI.main()

if __name__ == '__main__':
    main()