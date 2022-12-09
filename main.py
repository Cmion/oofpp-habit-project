import getopt
import sys

from lib.commandline_manager.commandline_manager import CommandlineManager


def main(argv):
    db_file = './habits.db'
    try:
        opts, args = getopt.getopt(argv, "d", ["database="])
    except getopt.GetoptError:
        print('usage: main.py -d <db-file-path> -o')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-d", "--database"):
            db_file = arg
    # print('Input file is ', db_file)

    command_line_manager = CommandlineManager(db_path=db_file)
    command_line_manager.start()


if __name__ == "__main__":
    main(sys.argv[1:])
