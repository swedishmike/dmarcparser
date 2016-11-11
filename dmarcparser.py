from  __future__ import print_function
import os
from modules.imap_connect import connect_and_find_new_reports
from modules.imap_connect import extract_files
from modules.splunk_connector import connect_to_splunk
from modules.splunk_connector import disconnect_from_splunk
from modules.splunk_connector import check_for_splunkindex
from modules.logconfig import set_up_logging


__version__ = "0.6"


SplunkHost = os.environ.get('SPLUNKHOST')
SplunkPort = os.environ.get('SPLUNKPORT')
SplunkUser = os.environ.get('SPLUNKUSER')
SplunkPassword = os.environ.get('SPLUNKPASSWORD')
SplunkIndex = os.environ.get('SPLUNKINDEX')


def initial_healthcheck():
    """ Sets up connection to Splunk etc"""
    logging.info('Starting the program')
    global service
    global target
    connect_to_splunk(SplunkHost, SplunkPort, SplunkUser, SplunkPassword)
    target = check_for_splunkindex(SplunkIndex)
    print(target)


def main():
    global logging
    print("Dmarc Parser ver", __version__)
    logging = set_up_logging()
    initial_healthcheck()
    imap = connect_and_find_new_reports(verbose=True)
    extract_files(target)
    disconnect_from_splunk()
    logging.info('Exiting the program')

if __name__ == '__main__':
    main()
