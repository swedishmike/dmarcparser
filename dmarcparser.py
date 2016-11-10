from  __future__ import print_function
import os
from modules.imap_connect import connect_and_find_new_reports
from modules.imap_connect import extract_files
from modules.splunk_connector import connect_to_splunk
from modules.splunk_connector import disconnect_from_splunk

__version__ = "0.5"

SplunkHost = os.environ.get('SPLUNKHOST')
SplunkPort = os.environ.get('SPLUNKPORT')
SplunkUser = os.environ.get('SPLUNKUSER')
SplunkPassword = os.environ.get('SPLUNKPASSWORD')
SplunkIndex = os.environ.get('SPLUNKINDEX')


if __name__ == '__main__':
    print ("Dmarc Parser ver", __version__)
    # imap = connect_and_find_new_reports(verbose=True)
    # extract_files()
    connect_to_splunk(SplunkHost, SplunkPort, SplunkUser, SplunkPassword)
    disconnect_from_splunk()