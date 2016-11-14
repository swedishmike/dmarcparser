from  __future__ import print_function
import os
import sys
# from modules.parseconfig import read_in_configfile
from ConfigParser import SafeConfigParser
from modules.imap_connect import connect_and_find_new_reports
from modules.imap_connect import send_files_to_parser
from modules.splunk_connector import connect_to_splunk
from modules.splunk_connector import disconnect_from_splunk
from modules.splunk_connector import check_for_splunkindex
from modules.logconfig import set_up_logging


__version__ = "0.8"


def read_in_configfile():
    global SplunkHost, SplunkPort, SplunkUser, SplunkPassword, SplunkIndex, hostname, username, password, parse_only_failed
    logging.info('Reading and parsing configuration file')
    print("[*] Importing configuration values")
    parser = SafeConfigParser()
    try:
        parser.read('dmarcparser.ini')
    except:
        print("\t[-] Could not find the configuration file dmarcparser.ini")
        logging.info('Could not find the configuration file.')
        sys.exit(1)


    try:
        SplunkHost = parser.get('Splunk Config', 'SplunkHost')
        SplunkPort = parser.get('Splunk Config', 'SplunkPort')
        SplunkUser = parser.get('Splunk Config', 'SplunkUser')
        SplunkPassword = parser.get('Splunk Config', 'SplunkPassword')
        SplunkIndex = parser.get('Splunk Config', 'SplunkIndex')
        hostname = parser.get('Imap Config', 'ImapServer')
        username = parser.get('Imap Config', 'ImapUser')
        password = parser.get('Imap Config', 'ImapPassword')
        parse_only_failed = parser.get('dmarcparser', 'ReportOnlyFailed')
    except:
        print("\t[-] Missing or incorrect value in dmarcparser.ini. Exiting.")
        logging.error('Could not find a specific variable in dmarcparser.ini', exc_info=True)
        sys.exit(1)

def initial_healthcheck():

    """ Sets up connection to Splunk etc"""
    global service
    global target
    connect_to_splunk(SplunkHost, SplunkPort, SplunkUser, SplunkPassword)
    target = check_for_splunkindex(SplunkIndex)


def main():
    global logging

    print("\n\nDmarc Parser ver", __version__, "\n")
    logging = set_up_logging()
    logging.info('Starting the program')
    read_in_configfile()
    initial_healthcheck()
    imap = connect_and_find_new_reports(hostname, username, password, parse_only_failed, target)
    disconnect_from_splunk()
    logging.info('Exiting the program')

if __name__ == '__main__':
    main()
