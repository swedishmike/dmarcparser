import imaplib
from imap_connect import open_connection
from pprint import pprint

with open_connection() as c:
    typ,  data = c.list()
    if typ == "OK":
        print("Response code:", typ)
        print("Response:")
        pprint(data)
    else:
        print("Something went wrong!")