import xml.etree.ElementTree as ET
import datetime

if __name__ == '__main__':
    # file_to_parse = "bzone.it!cloud.sophos.com!0!1478085339.xml"
    file_to_parse = "google.com!sophos.com!1477958400!1478044799.xml"
    tree = ET.parse(file_to_parse)
    report = tree.getroot()

    report_organisation = report.find('report_metadata/org_name').text
    report_id = report.find('report_metadata/report_id').text
    report_contact = report.find('report_metadata/email').text
    report_startdate = datetime.datetime.fromtimestamp(int(report.find('report_metadata/date_range/begin').text)).strftime('%Y-%m-%d %H:%M:%S')
    report_enddate = datetime.datetime.fromtimestamp(int(report.find('report_metadata/date_range/end').text)).strftime('%Y-%m-%d %H:%M:%S')
    print("Organisation: %s Email: %s\nReport id: %s Start date: %s End date: %s" % (report_organisation, report_contact, report_id, report_startdate, report_enddate))

    record_list = report.findall('record')

    print("Total records: ", len(record_list))

    for record in record_list:
        print(record.find('row/source_ip').text)
        print(record.find('identifiers/header_from').text)
        if record.find('row/policy_evaluated/dkim').text != "pass":
            print("DKIM failed!")
        else:
            print("DKIM passed")
        if record.find('row/policy_evaluated/spf').text != "pass":
            print("SPF failed!")
        else:
            print("SPF passed!")