from __future__ import unicode_literals

import requests
import json
from bs4 import BeautifulSoup


def records_csv(from_date, to_date, report_type):
    options = {
        "cboFilerType": "PCC",
        "txtFromDate": from_date,
        "txtToDate": to_date,
        "optReportOption": report_type,
        "cboSort1": "agyname, ",
        "filing_year": "",
        "optFormat": "CSV",
    }

    get_some_cookies_from_url = "http://www.ocf.dc.gov/serv/download.asp"

    s = requests.Session()

    s.post(get_some_cookies_from_url, options).raise_for_status()

    download_url = 'http://www.ocf.dc.gov/serv/download_conexp.asp'
    r = s.post(download_url, options)
    r.raise_for_status()

    return r.text

def available_years():
    js_with_years_in_it = 'http://geospatial.dcgis.dc.gov/ocf/js/process.js'
    r = requests.get(js_with_years_in_it)

    years_line = r.text.splitlines()[3]
    # This line looks like like:
    # var m_Interface_Control = [{ "year": "2010", "defaultoffice": "Mayor", "showparty": "yes", "defaultparty": "Democratic" }, { "year": "2011", "defaultoffice": "Council At-Large", "showparty": "no", "defaultparty": "" }, { "year": "2012", "defaultoffice": "Council At-Large", "showparty": "no", "defaultparty": "" }, { "year": "2013", "defaultoffice": "Council At-Large", "showparty": "no", "defaultparty": ""}, { "year": "2014", "defaultoffice": "Council At-Large", "showparty": "no", "defaultparty": ""}];
    years_json_text = years_line.lstrip('var m_Interface_Control =').rstrip(';')
    # Now we have just the json:
    # [{ "year": "2010", "defaultoffice": "Mayor", "showparty": "yes", "defaultparty": "Democratic" }, { "year": "2011", "defaultoffice": "Council At-Large", "showparty": "no", "defaultparty": "" }, { "year": "2012", "defaultoffice": "Council At-Large", "showparty": "no", "defaultparty": "" }, { "year": "2013", "defaultoffice": "Council At-Large", "showparty": "no", "defaultparty": ""}, { "year": "2014", "defaultoffice": "Council At-Large", "showparty": "no", "defaultparty": ""}]
    years_json = json.loads(years_json_text)

    # then we just want to return a list of the years
    return [int(year['year']) for year in years_json]

def offices():
    html_with_offices_in_it = 'http://geospatial.dcgis.dc.gov/ocf/'
    r = requests.get(html_with_offices_in_it)
    soup = BeautifulSoup(r.text)

    office_option_elements = soup.find(id='SearchByOffices')('option')
    # sort them by their form value, so they look all nice and ordered
    office_option_elements.sort(key=lambda e: int(e['value']))

    return [e.text for e in office_option_elements]
