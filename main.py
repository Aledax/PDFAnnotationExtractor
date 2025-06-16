import sys

from lib.lib import *

if __name__ == '__main__':

    if len(sys.argv) > 0:

        file_name = sys.argv[1]
        text = extract_annotated_text(file_name)
        write_annotated_text(file_name, text)

        input('Complete. Press Enter to continue...')