import xml.etree.ElementTree as ET
import datetime
import sys
import logging

class dmarc_rua_parser:
    def __init__(self, file_to_parse, target):
        self.file_to_parse = file_to_parse
        self.target = target
        self.parse_rua_file(self.file_to_parse, target)

    def publish_to_splunk(self, sourcetype, submitstring, target):
        try:
            target.submit(submitstring, sourcetype=sourcetype)
        except:
            print("\t[-] Something unknown went wrong when submitting to Splunk. Exiting.")
            logging.error('Could not submit to Splunk', exc_info=True)
            sys.exit(1)


    def parse_rua_file(self, file_to_parse, target):
        tree = ET.parse(file_to_parse)
        report = tree.getroot()

        report_only_failed = False

        report_organisation = report.find('report_metadata/org_name').text
        report_id = report.find('report_metadata/report_id').text
        report_contact = report.find('report_metadata/email').text
        report_startdate = datetime.datetime.fromtimestamp(
            int(report.find('report_metadata/date_range/begin').text)).strftime('%Y-%m-%d %H:%M:%S')
        report_enddate = datetime.datetime.fromtimestamp(
            int(report.find('report_metadata/date_range/end').text)).strftime('%Y-%m-%d %H:%M:%S')

        all_records = report.findall('record')
        logging.info('File: %s Total Records: %s' % (file_to_parse, len(all_records)))
        # print("Total records: ", len(all_records))

        for record in all_records:
            if report_only_failed:
                reportable = False
                if record.find('row/policy_evaluated/dkim').text != "pass":
                    reportable = True
                else:
                    pass
                if record.find('row/policy_evaluated/spf').text != "pass":
                    reportable = True
                else:
                    pass
            else:
                reportable = True

            if reportable:
                sourcetype = "dmarc_rua"

                try:
                    auth_dkim_domain = record.find('auth_results/dkim/domain').text
                except:
                    auth_dkim_domain = "None"
                try:
                    auth_spf_domain = record.find('auth_results/spf/domain').text
                except:
                    auth_spf_domain = "None"
                try:
                    auth_dkim_result = record.find('auth_results/dkim/result').text
                except:
                    auth_dkim_result = "None"
                try:
                    auth_spf_result = record.find('auth_results/spf/result').text
                except:
                    auth_spf_result = "None"


                submitstring = (
                    "org_name=\"%s\" "
                    "contact=\"%s\" "
                    "report_id=\"%s\" "
                    "report_startdate=\"%s\" "
                    "report_enddate=\"%s\" "
                    "srcip=\"%s\" "
                    "header_from=\"%s\" "
                    "policy_dkim=\"%s\" "
                    "policy_spf=\"%s\" "
                    "dkim_domain=\"%s\" "
                    "dkim_result=\"%s\" "
                    "spf_domain=\"%s\" "
                    "spf_result=\"%s\" "
                    % (report_organisation, report_contact, report_id, report_startdate, report_enddate,
                       record.find('row/source_ip').text, record.find('identifiers/header_from').text,
                       record.find('row/policy_evaluated/dkim').text,record.find('row/policy_evaluated/spf').text,
                       auth_dkim_domain, auth_dkim_result,
                       auth_spf_domain, auth_spf_result))

                # print("Publishing to Splunk")
                # print(sourcetype, submitstring)
                self.publish_to_splunk(sourcetype, submitstring, target)
            else:
                pass



if __name__ == '__main__':
    print("This program should not be run on its own, it should be called from dmarcparser.py. Exiting.")
    sys.exit(1)