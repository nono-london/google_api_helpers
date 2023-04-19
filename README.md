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

#### Enable "APIs and services"

You have to enable the API/Services, depending on your use

* to use GSheet:
    * click on "ENABLE APIS AND SERVICES" in the "APIs & Services" Section
      ![alt-text](/README_pics/enable_apis.PNG "optional-title")
    * Click on "Google Sheets API" in the "Google Workspace" section
      ![alt-text](/README_pics/enable_gsheet_api.PNG "optional-title")

* to use Gmail:
    * click on "ENABLE APIS AND SERVICES" in the "APIs & Services" Section
      ![alt-text](/README_pics/enable_apis.PNG "optional-title")
    * Click on "Gmail API" in the "Google Workspace" section
      ![alt-text](/README_pics/enable_gmail_api.PNG "optional-title")

# Gmail API

### Definitions

* user_id: needs to be the email that has been authorized or explore delegation

### Limits

Per-method quota usage
The number of quota units consumed by a request varies depending on the method called. The following table outlines the
per-method quota unit usage:

#### Method	Quota Units

drafts.create 10
drafts.delete 10
drafts.get 5
drafts.list 5
drafts.send 100
drafts.update 15
getProfile 1
history.list 2
labels.create 5
labels.delete 5
labels.get 1
labels.list 1
labels.update 5
messages.attachments.get 5
messages.batchDelete 50
messages.delete 10
messages.get 5
messages.import 25
messages.insert 25
messages.list 5
messages.modify 5
messages.send 100
messages.trash 5
messages.untrash 5
settings.delegates.create 100
settings.delegates.delete 5
settings.delegates.get 1
settings.delegates.list 1
settings.filters.create 5
settings.filters.delete 5
settings.filters.get 1
settings.filters.list 1
settings.forwardingAddresses.create 100
settings.forwardingAddresses.delete 5
settings.forwardingAddresses.get 1
settings.forwardingAddresses.list 1
settings.getAutoForwarding 1
settings.getImap 1
settings.getPop 1
settings.getVacation 1
settings.sendAs.create 100
settings.sendAs.delete 5
settings.sendAs.get 1
settings.sendAs.list 1
settings.sendAs.update 100
settings.sendAs.verify 100
settings.updateAutoForwarding 5
settings.updateImap 5
settings.updatePop 100
settings.updateVacation 5
stop 50
threads.delete 20
threads.get 10
threads.list 10
threads.modify 10
threads.trash 10
threads.untrash 10
watch 100

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

# Useful Git commands

* remove files git repository (not the file system)
    ```
    git rm --cached <path of file to be removed from git repo.>
    git commit -m "Deleted file from repository only"
    git push
    ```
* cancel command:
    ```
    git restore --staged .
    ```
* create tags/versions on GitHub
    ```
    git tag <version_number>
    git push origin <version_number>

    ```
  
### Google API

* [Create Google API credentials](https://console.cloud.google.com/flows/enableapi?apiid=sheets.googleapis.com)
* [Create Google app account - stackoverflow](https://stackoverflow.com/questions/74839142/google-sheet-api-request-had-insufficient-authentication-scopes/74956230#74956230)
* [Gmail API docs](https://developers.google.com/gmail/api/quickstart/python)
* [Gmail API tutorial](https://skillshats.com/blogs/send-and-read-emails-with-gmail-api/)
* [Clear whole sheet - stackoverflow](https://stackoverflow.com/questions/58293066/using-python-to-clear-all-the-cell-values-in-google-sheet-before-adding-data/76023704#76023704)
* [Clear sheet - Google tutorial](https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/clear)
* [Access sheet - Google tutorial](https://developers.google.com/sheets/api/quickstart/python)
* [Write sheet - Google tutorial](https://developers.google.com/sheets/api/guides/values)
* [Create a spreadsheet](https://developers.google.com/sheets/api/guides/create)

* [python-dotenv](https://pypi.org/project/python-dotenv/)

