google_api_helpers
===
Helps you connect to your G documents, and deals with the Google API

# Installation

### Python libs

```
pip install -r requirements.txt
```

### Create a ".env" file in the root folder

This file should contain a G_SHEET_ID variable for the tests to run properly
It should look something like this:

file .env

```
G_SHEET_ID = 'examplesdsdsd123123123'
```

in path to file (same path as .env_example):

```
google_api_helpers/.env
```

### Google Authentication

In order to use the Google API:

* create an App in your Google Cloud
* Save the credentials file as "g_credentials.json" in the folder:

```
google_api_helpers/google_api_helpers/g_credentials/g_credentials.json
```

# Run tests

Running allows you to check that the installation process worked
For the tests to run properly you need to have:

* credential key saved in g_credentials folder as g_credentials.json
* access to a GSheet with writing and reading rights.
* Save the GSheet spreadsheet_id in the .env file

# TODO

* Add drive use
* Explain usage in docs
* [Create setup.py correctly](https://setuptools.pypa.io/en/latest/setuptools.html#including-data-files)

# Sources and useful links

### Google API
* [Create Google API credentials](https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com
)
* [Create Google app account - stackoverflow](https://stackoverflow.com/questions/74839142/google-sheet-api-request-had-insufficient-authentication-scopes/74956230#74956230)
* [Clear whole sheet - stackoverflow](https://stackoverflow.com/questions/58293066/using-python-to-clear-all-the-cell-values-in-google-sheet-before-adding-data/76023704#76023704)
* [Clear sheet - Google tutorial](https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/clear)
* [Access sheet - Google tutorial](https://developers.google.com/sheets/api/quickstart/python)
* [Write sheet - Google tutorial](https://developers.google.com/sheets/api/guides/values)
* [Create a spreadsheet](https://developers.google.com/sheets/api/guides/create)

* [python-dotenv](https://pypi.org/project/python-dotenv/)

