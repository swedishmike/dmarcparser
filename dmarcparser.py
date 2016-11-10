from  __future__ import print_function
from modules.imap_connect import connect_and_find_new_reports
from modules.imap_connect import extract_files
__version__ = "0.5"

if __name__ == '__main__':
    print ("Dmarc Parser ver", __version__)
    imap = connect_and_find_new_reports(verbose=True)
    extract_files()