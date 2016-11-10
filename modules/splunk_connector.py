import sys
import splunklib.client as client
import os





def connect_to_splunk(SplunkHost, SplunkPort, SplunkUser, SplunkPassword):
    """ Sets up the connection to the Splunk instance """
    global service
    print "[*] Connecting to Splunk"
    try:
        service = client.connect(
            host=SplunkHost,
            port=SplunkPort,
            username=SplunkUser,
            password=SplunkPassword)
    except client.AuthenticationError:
        print "\t[-] Login to Splunk failed - check your settings"
        logging.error('Login to Splunk failed.', exc_info=True)
        sys.exit(1)
    except client.socket.error:
        print "\t[-] Connection to Splunk failed - check your settings"
        logging.error('Connection to Splunk failed.', exc_info=True)
        sys.exit(1)
    except:
        print "\t[-] Something unknown went wrong when connecting to Splunk"
        logging.error('Something went wrong when connecting to Splunk.',
                      exc_info=True)
        sys.exit(1)
    else:
        print "\t[+] Connected to Splunk"


def disconnect_from_splunk():
    service.logout()
    print("Disconnected from Splunk.")

if __name__ == '__main__':
    print("Should not be started on its own - please run \'dmarcparser.py\' instead.")
    sys.exit(1)