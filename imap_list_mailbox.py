import imaplib
from imap_connect import connect_and_find_new_reports
from pprint import pprint

with connect_and_find_new_reports() as c:
    typ,  data = c.list()
    if typ == "OK":
        print("Response code:", typ)
        print("Response:")
        pprint(data)
    else:
        print("Something went wrong!")