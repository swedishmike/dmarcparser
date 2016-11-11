# dmarcparser
A quick and dirty implementation to get DMARC rua reports into Splunk for further analysis

Reads the emails from IMAP, transmogrifies the data and outputs it to Splunk. Simples.

## Requirements

* Python 2.7 (Since the Splunk SDK does not support Python 3 yet)
* Splunk SDK.
* A Splunk installation that can accept conncections via the SDK.
* A IMAP server that accepts connections on port 993 for secure connections.
* You will of course also need a dmarc record defined in your dns zone. If you don't know how to do that - Google is your friend. ;-)

## Installation and configuration

### Installation
- Clone this repo onto your host
- Change direcotory into the program directory and run `pip install -r requirements.txt`

### Configuration

Copy the `dmarcparser.ini.original` file to `dmarcparser.ini` and edit the following settings to suit your environment.

~~~~
[Splunk Config]
SplunkHost =
SplunkPort =
SplunkUser =
SplunkPassword =
SplunkIndex =
~~~~

~~~~
[Imap Config]
ImapServer =
ImapUser =
ImapPassword =
~~~~

~~~~
[dmarcparser]
ReportOnlyFailed = True
~~~~

These settings should be pretty self explanatory with the possible exception of `ReportOnlyFailed`. If that is set to `False` it will parse and transfer all entries in the reports, not only failed ones. That way you have all the data in Splunk and can do your own parsing instead of relying on the parsing in this program.

## Troubleshooting

By default the program logs errors and informational entries into the file `dmarcparser.log`. Review this one to try and find out why things are not working as expected.
 
If you need even more logging, edit the file `modules/logconfig.py` and in the snippet below, change the level from `INFO` to `DEBUG`.  

~~~~
        'loggers': {
            '': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True
            }
~~~~

For any other problems or bugs - open an issue here on Github and I'll try to assist.
###### Disclaimer: This program does not come with any guarantees that it will actually work. Best efforts will be made to make it work as well as possible though.
