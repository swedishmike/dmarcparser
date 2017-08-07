import email
import glob
import gzip
import imaplib
import logging
import os
import sys
import zipfile

from parse_report import dmarc_rua_parser

zipfiles = []
gzfiles = []
packdir = "packed/"
unpackdir = "unpacked/"


def connect_and_find_new_reports(hostname, username, password, target, deleteemails):
    # Check if the necessary directories are there, if not - create them
    if not os.path.exists(unpackdir):
        try:
            os.makedirs(unpackdir)
        except:
            logging.error('Could not create directory', exc_info=True)
            print("\t[-] Could not create a necessary directory.")
            sys.exit(1)
    if not os.path.exists(packdir):
        try:
            os.makedirs(packdir)
        except:
            logging.error('Could not create directory', exc_info=True)
            print("\t[-] Could not create a necessary directory.")
            sys.exit(1)

    # Connect to the server
    print "[*] Connecting to the IMAP server"
    logging.info('Connecting to IMAP server %s', hostname)
    try:
        imap = imaplib.IMAP4_SSL(hostname)
    except:
        print "\t[-] Connection to the IMAP server failed - check your settings"
        logging.error('Something went wrong when connecting to the IMAP server.', exc_info=True)

    # Login to our account
    try:
        imap.login(username, password)
    except:
        print "\t[-] Connection to the IMAP server failed - check your settings"
        logging.error('Something went wrong when connecting to the IMAP server.', exc_info=True)

    # Select the Inbox
    try:
        imap.select('INBOX')
    except:
        print "\t[-] Connection to the IMAP server failed - check your settings"
        logging.error('Something went wrong when connecting to IMAP server.', exc_info=True)

    # Look for unread emails
    print "\t[+] Checking for unread emails"
    logging.info('Checking for unread emails')
    typ, unread_emails = imap.search(None, 'UNSEEN')

    # Loop through emails and grab attachments
    if len(unread_emails[0].split()) > 0:
        print("\t[+] Parsing attachments")
        logging.info('Parsing attachments')
    for number in unread_emails[0].split():
        # Get the current email
        typ, data = imap.fetch(number, '(RFC822)')
        # message = email.message_from_bytes(data[0][1]) <--- Python3
        message = email.message_from_string(data[0][1])
        #
        for part in message.walk():
            attach_name = part.get_filename()
            if attach_name:
                attach_dest = packdir + attach_name
                if not (attach_name.endswith('.zip') or attach_name.endswith('.gz')):
                    logging.info('Ignoring non-zip or non-gz attachment "{0}"'.format(attach_name))
                    continue
                try:
                    attach_data = part.get_payload(decode=True)
                except binascii.Error:
                    logging.error('Could not decode attachment "{0}"'.format(attach_name))
                    continue

                with open(attach_dest, "wb") as fd:
                    try:
                        fd.write(attach_data)
                    except:
                        print("Attachment data:", attach_data)
                        if os.path.isfile(attach_dest):
                            logging.error('File already exists %s', attach_dest)
                        logging.error('Could not write %s', attach_data, exc_info=True)
                if attach_name.endswith('.zip'):
                    extract_zip_file(attach_dest, target)
                else:
                    extract_gz_file(attach_dest, target)
        #
        if deleteemails == "Yes":
           logging.info('Deleting the email from server')
           imap.store(number, '+FLAGS', '\\Deleted')
           imap.expunge()


    imap.close()
    imap.logout()
    logging.info('Disconnected from IMAP server')
    print "[*] Disconnected from IMAP server"
    return imap


def extract_zip_file(file, target):
    try:
        zip_ref = zipfile.ZipFile(file, 'r')
    except:
            # print("Something went wrong when opening the file")
            logging.error('Something went wrong when opening a file', exc_info=True)
            pass
    zip_ref.extractall(unpackdir)
    zip_ref.close()
    os.remove(file)
    send_files_to_parser(target)
    return


def extract_gz_file(file, target):
    directory, filename = os.path.split(file)
    xmlfile, extension = os.path.splitext(filename)
    newfilelocation = unpackdir + xmlfile
    # Decompress the gz file
    try:
        compressedfile = gzip.GzipFile(file)
    except:
        # print("Something went wrong when opening the file")
        logging.error('Something went wrong when opening a file', exc_info=True)
        pass
    content = compressedfile.read()
    compressedfile.close()

    # Write the new decompressed file in the unpack directory
    decompressedfile = open(newfilelocation, 'wb')
    try:
        decompressedfile.write(content)
    except:
        logging.error('Something went wrong when saving a file', exc_info=True)
    decompressedfile.close()

    # Delete the compressed file
    os.remove(file)
    send_files_to_parser(target)
    return


def send_files_to_parser(target):
    # print("Starting to parse files")
    if len (glob.glob('unpacked/*.xml')) > 0:
        for file in glob.glob('unpacked/*.xml'):
            dmarc_rua_parser(file, target)
            os.remove(file)
    else:
        print("No files to parse")


if __name__ == '__main__':
    print("This program should not be run on its own, it should be called from dmarcparser.py. Exiting.")
    sys.exit(1)
