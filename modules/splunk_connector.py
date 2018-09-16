import logging
import sys

import splunklib.client as client


def connect_to_splunk(SplunkHost, SplunkPort, SplunkUser, SplunkPassword):
    """ Sets up the connection to the Splunk instance """
    global service
    logging.info("Connecting to Splunk")
    print "[*] Connecting to Splunk"
    try:
        service = client.connect(
            host=SplunkHost,
            port=SplunkPort,
            username=SplunkUser,
            password=SplunkPassword,
            autologin=True,
        )
    except client.AuthenticationError:
        print "\t[-] Login to Splunk failed - check your settings"
        logging.error("Login to Splunk failed.", exc_info=True)
        sys.exit(1)
    except client.socket.error:
        print "\t[-] Connection to Splunk failed - check your settings"
        logging.error("Connection to Splunk failed.", exc_info=True)
        sys.exit(1)
    except:
        print "\t[-] Something unknown went wrong when connecting to Splunk"
        logging.error("Something went wrong when connecting to Splunk.", exc_info=True)
        sys.exit(1)
    else:
        logging.info("Connected to Splunk.")
        print "\t[+] Connected to Splunk"
        return service


def disconnect_from_splunk():
    service.logout()
    logging.info("Disconnected from Splunk")
    print ("[*] Disconnected from Splunk.")


def check_for_splunkindex(SplunkIndex):
    """ Makes sure that the index we want to use exists. """
    indexes = service.indexes
    indexlist = []

    for index in indexes:
        indexlist.append(index.name)

    if SplunkIndex in indexlist:
        print "\t[+] The specified Splunk Index exists"
        target = service.indexes[SplunkIndex]
        return target

    else:
        print "\t[-] Can't find the specified Splunk Index:", SplunkIndex
        logging.error("Cannot find the specified Splunk Index: %s", SplunkIndex)
        sys.exit(1)


if __name__ == "__main__":
    print ("Should not be started on its own - please run 'dmarcparser.py' instead.")
    sys.exit(1)
