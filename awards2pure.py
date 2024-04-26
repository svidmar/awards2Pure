import csv
import json
import requests
from datetime import datetime
from getpass import getpass
from time import sleep

# Constants
CSV_FILE_PATH = 'data.csv'
LOG_FILE_PATH = f'logfile_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'

def load_csv_data(csv_path):
    """ Load data from CSV file. """
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        print("CSV data loaded successfully.")
        return list(csv.DictReader(csvfile, delimiter=';'))

def reformat_date(date_string):
    """ Convert date string from d-m-Y to Y-m-d format; return original if format is invalid. """
    try:
        return datetime.strptime(date_string, '%d-%m-%Y').strftime('%Y-%m-%d')
    except ValueError:
        return date_string

def construct_json_payload(row):
    return {
        "awardHolders": [
            {
                "typeDiscriminator": "InternalAwardHolderAssociation",
                "role": {"uri": "/dk/atira/pure/award/roles/award/pi"},
                "person": {"systemName": "Person", "uuid": row.get('Personuuid', '')},
                "organizations": [
                    {"systemName": "Organization", "uuid": row.get('InstitutUUID', '')},
                    {"systemName": "Organization", "uuid": row.get('FakultetUUID', '')}
                ]
            }
        ],
        "awardDate": reformat_date(row.get('awardDate', '')),
        "type": {"uri": row.get('typeuri', '')},
        "expectedPeriod": {
            "startDate": reformat_date(row.get('startDate', '')),
            "endDate": reformat_date(row.get('endDate', ''))
        },
        "identifiers": [
            {
                "typeDiscriminator": "ClassifiedId",
                "id": row.get('projektid', ''),
                "type": {"uri": "/dk/atira/pure/upm/classifiedsource/projectid"}
            }
        ],
        "fundings": [
            {
                "funder": {"uuid": row.get('bevillingsgiveruuid', ''), "systemName": "ExternalOrganization"},
                "awardedAmount": {"value": row.get('funds', '')},
                "visibility": {"key": "BACKEND"},
                "typeDiscriminator": "AwardFinancialFundingAssociation"
            }
        ],
        "organizations": [
            {"uuid": row.get('InstitutUUID', ''), "systemName": "Organization"},
            {"uuid": row.get('FakultetUUID', ''), "systemName": "Organization"}
        ],
        "managingOrganization": {"uuid": row.get('InstitutUUID', ''), "systemName": "Organization"},
        "title": {"en_GB": row.get('title', '')},
        "visibility": {"key": "BACKEND"},
        "typeDiscriminator": "AwardManagementAward"
    }

def send_request(session, data, api_url, api_key):
    """ Send API request using session and return status code and response text. """
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    json_data = json.dumps(data)
    print("Final JSON Payload:", json_data)  # Debugging line
    try:
        response = session.put(api_url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"Error from API: {response.text}")  # Print detailed error message
        return response.status_code, response.text
    except Exception as e:
        print(f"HTTP request failed: {e}")
        return None, None

def main():
    api_url = input("Enter API URL: ")
    api_key = getpass("Enter API key: ")
    
    # Establish a session for the initial server connection using username and password
    session = requests.Session()
    username = input("Enter basic auth username: ")
    password = getpass("Enter basic auth password: ")
    session.auth = (username, password)  # Set basic auth for initial connection

    rows = load_csv_data(CSV_FILE_PATH)
    with open(LOG_FILE_PATH, 'w') as logfile:
        for row in rows:
            sleep(1)  # Delay each API request by one second
            data_to_send = construct_json_payload(row)
            status_code, response = send_request(session, data_to_send, api_url, api_key)
            log_entry = f"{row['projektid']}, {status_code}\n"
            logfile.write(log_entry)
            print(f"Logged: {log_entry.strip()}")

if __name__ == "__main__":
    main()
