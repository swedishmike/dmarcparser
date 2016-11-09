import imaplib
import os

hostname = os.environ.get('IMAPSERVER')
username = os.environ.get('IMAP_USER')
password = os.environ.get('IMAP_PASSWORD')

def open_connection(verbose=False):
    # Connect to the server
    if verbose:
        print('Connecting to', hostname)
    connection = imaplib.IMAP4_SSL(hostname)

    # Login to our account
    if verbose:
        print('Logging in as', username)
    connection.login(username, password)
    return connection


if __name__ == '__main__':
    with open_connection(verbose=True) as c:
        print(c)
