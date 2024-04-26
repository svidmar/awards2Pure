Script Documentation: Awards Data Submission to API
Overview
This script is designed to read award data from a CSV file, construct JSON payloads, and send these payloads to a specified API. It's intended for automating the process of updating award information in a database via an API, handling data transformation, and logging the outcome of each API request.

Requirements
Python 3.6 or higher
External libraries: requests, which can be installed via pip:
bash
Copy code
pip install requests
Setup
Before running the script, ensure that the following files and settings are correctly configured:

A CSV file named data.csv in the script's directory with award data.
The script requires API credentials and endpoint details which will be requested upon execution.
Functions Description
load_csv_data(csv_path)
Purpose: Loads data from a CSV file and skips empty lines.
Parameters:
csv_path: The file path to the CSV file.
Returns: A list of dictionaries where each dictionary represents a row from the CSV.
reformat_date(date_string)
Purpose: Converts date strings from "d-m-Y" format to "Y-m-d". If the date is invalid, it returns the original string.
Parameters:
date_string: The date string to reformat.
Returns: A string representing the reformatted date or the original string if invalid.
construct_json_payload(row)
Purpose: Constructs a JSON payload suitable for API submission based on the row data.
Parameters:
row: A dictionary containing data of a single row from the CSV.
Returns: A dictionary structured as a JSON object ready for API submission.
send_request(session, data, api_url, api_key)
Purpose: Sends a PUT request to the API with the JSON data.
Parameters:
session: An instance of requests.Session configured with authentication.
data: The JSON payload to be sent.
api_url: The endpoint URL of the API.
api_key: The API key for authorization.
Returns: A tuple containing the status code and response text from the API.
Main Process
User Input: The script prompts for the API URL and API key.
Session Initialization: Initializes a requests.Session with basic authentication credentials provided by the user.
Data Loading: Reads and processes data from data.csv.
Data Processing: For each row in the CSV, constructs a JSON payload and sends it to the API. It logs the response and status code to a logfile.
Logging: Details of each request's outcome are logged to a file named logfile_YYYYMMDD_HHMMSS.txt, where the datetime component is generated at runtime.
Execution
To run the script, execute it from the command line:

bash
Copy code
python awards2pure.py
Ensure that you have the necessary permissions and correct path to data.csv. The script will handle data transformation, API submission, and logging automatically.