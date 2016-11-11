import sys
from ConfigParser import SafeConfigParser

global parse_only_failed

def read_in_configfile():

    print "[*] Importing configuration values"
    parser = SafeConfigParser()
    try:
        parser.read('dmarcparser.ini')
    except:
        print "\t[-] Could not find the Configuration file dmarcparser.ini"
        sys.exit(1)
    try:
        parse_only_failed = parser.get('dmarcparser', 'ReportOnlyFailed')
    except:
        print "\t[-] Missing or incorrect value in dmarcparser.ini. Exiting."
        logging.error('Could not find a specific variable in dmarcparser.ini', exc_info=True)
        sys.exit(1)
    print(parse_only_failed)
    return (parse_only_failed)

if __name__ == '__main__':
    print("Should not be started on its own - please run \'dmarcparser.py\' instead.")
    sys.exit(1)