# awards2Pure

## Overview
This script is designed to read award data from a CSV file, construct JSON payloads, and send these payloads to the Elsevier Pure API. It's intended for automating the process of updating award information via API, handling data transformation, and logging the outcome of each API request.

## Dependencies

To run this script, you'll need Python 3.x and several libraries which you can install using pip:

- `requests`: For making HTTP requests.
- `csv` and `json`: For CSV file operations and JSON handling.
- `datetime`: For manipulating dates and times.
- `getpass`: For secure password input.
- `time`: For handling delays between requests.

Before running the script, ensure that the following files and settings are correctly configured:

- A CSV file named `data.csv` in the script's directory with award data.

The script requires API credentials and endpoint details which will be requested upon execution.