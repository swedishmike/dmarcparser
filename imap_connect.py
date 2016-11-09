import imaplib
import os
import email


hostname = os.environ.get('IMAPSERVER')
username = os.environ.get('IMAP_USER')
password = os.environ.get('IMAP_PASSWORD')
zipfiles = []
gzfiles = []

def connect_and_find_new_reports(verbose=False):

    packdir = "packed/"

    # Connect to the server
    if verbose:
        print('Connecting to', hostname)
    imap = imaplib.IMAP4_SSL(hostname)

    # Login to our account
    if verbose:
        print('Logging in as', username)
    imap.login(username, password)

    # Select the Inbox
    imap.select('INBOX')

    # Look for unread emails
    typ, unread_emails = imap.search(None, 'UNSEEN')

    # Loop through emails and grab attachments
    for number in unread_emails[0].split():
        # print(number)
        # Get the current email
        typ, data = imap.fetch(number, '(RFC822)')

        # print(data)
        message = email.message_from_bytes(data[0][1])
        # message = email.message_from_string(data[0][1]) <--- When I move to Python2
        #
        for part in message.walk():
            attach_name = part.get_filename()
            if attach_name:
                attach_dest = packdir + attach_name
                if not (attach_name.endswith('.zip') or attach_name.endswith('.gz')):
                    print("Don't have a useful file attached")
                    # log('ignoring non-zip attachment "{0}"'.format(attach_name))
                    continue
                # if not attach_name.endswith('.gz'):
                #     print("Don't have a .gz file attached")
                #     # log('ignoring non-zip attachment "{0}"'.format(attach_name))
                #     passdiur
                try:
                    attach_data = email.base64mime.decode(part.get_payload())
                except binascii.Error:
                    print("Could not decode attachment")
                    # log('could not decode attachment "{0}"'.format(attach_name))
                    continue

                with open(attach_dest, "wb") as fd:
                    fd.write(attach_data)
                if attach_name.endswith('zip'):
                    zipfiles.append(attach_dest)
                else:
                    gzfiles.append(attach_dest)

    # print(unread_emails)
    # print(zipfiles)
    # print(gzfiles)
    # for file in gzfiles:
    #     print(file)

    return imap

def extract_files(verbose=False):
    if len(zipfiles) > 0:
        for file in zipfiles:
            print(file)
    else:
        print("No zip files")
    if len(gzfiles) > 0:
        for file in gzfiles:
            print(file)
    else:
        print("No gz files")

if __name__ == '__main__':
    with connect_and_find_new_reports(verbose=True) as c:
        print(c)
    extract_files()