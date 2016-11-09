import xml.etree.ElementTree as ET
import datetime

class dmarc_rua_parser:
    def __init__(self, file_to_parse):
        self.file_to_parse = file_to_parse
        self.parse_rua_file(self.file_to_parse)

    def parse_rua_file(self, file_to_parse):
        tree = ET.parse(file_to_parse)
        report = tree.getroot()

        report_organisation = report.find('report_metadata/org_name').text
        report_id = report.find('report_metadata/report_id').text
        report_contact = report.find('report_metadata/email').text
        report_startdate = datetime.datetime.fromtimestamp(
            int(report.find('report_metadata/date_range/begin').text)).strftime('%Y-%m-%d %H:%M:%S')
        report_enddate = datetime.datetime.fromtimestamp(
            int(report.find('report_metadata/date_range/end').text)).strftime('%Y-%m-%d %H:%M:%S')

        all_records = report.findall('record')
        print("Total records: ", len(all_records))

        for record in all_records:
            reportable = False
            if record.find('row/policy_evaluated/dkim').text != "pass":
                reportable = True
            else:
                pass
            if record.find('row/policy_evaluated/spf').text != "pass":
                reportable = True
            else:
                pass
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
                    "source_ip=\"%s\" "
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
                print(sourcetype, submitstring)

            else:
                pass

if __name__ == '__main__':
    # file_to_parse = "bzone.it!cloud.sophos.com!0!1478085339.xml"
    # file_to_parse = "google.com!sophos.com!1477958400!1478044799.xml"
    # file_to_parse = "rabobank.nl!cloud.sophos.com!1478149205!1478235604.xml"
    file_to_parse = "yahoo.com!sophos.com!1478044800!1478131199.xml"

    dmarc_rua_parser(file_to_parse)