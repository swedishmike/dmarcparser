import xml.etree.ElementTree as ET
import datetime

if __name__ == '__main__':
    file_to_parse = "bzone.it!cloud.sophos.com!0!1478085339.xml"
    tree = ET.parse(file_to_parse)
    report = tree.getroot()

    report_organisation = report.find('report_metadata/org_name').text
    report_id = report.find('report_metadata/report_id').text
    report_startdate = datetime.datetime.fromtimestamp(int(report.find('report_metadata/date_range/begin').text)).strftime('%Y-%m-%d %H:%M:%S')
    report_enddate = datetime.datetime.fromtimestamp(int(report.find('report_metadata/date_range/end').text)).strftime('%Y-%m-%d %H:%M:%S')
    print("Organisation: %s Report id: %s Start date: %s End date: %s" % (report_organisation, report_id, report_startdate, report_enddate))

