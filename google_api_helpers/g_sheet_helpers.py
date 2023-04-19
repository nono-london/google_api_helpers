import os
from pprint import pprint
from typing import (Optional, List, Union, Dict)

import pandas as pd
from googleapiclient import discovery
from googleapiclient.errors import HttpError

from google_api_helpers.app_config import load_env_variables
from google_api_helpers.g_auth_helpers import (GAuthHandler, AuthScope)
from google_api_helpers.misc_helpers import build_sheet_range


class GSheetHandler(GAuthHandler):
    def __init__(self, auth_scopes: Union[List[AuthScope], None],
                 spreadsheet_id: Optional[str] = None):
        super().__init__(auth_scopes)

        # get authorization
        self.get_g_auth()
        # if None load from .env variables
        if spreadsheet_id is None:
            load_env_variables()
            self.spreadsheet_id = os.getenv('G_SHEET_ID')
        else:
            self.spreadsheet_id = spreadsheet_id

    def get_sheet_desc(self):
        # check that we are requesting a GSheet Auth
        if AuthScope.SpreadSheet.value not in self.auth_scopes:
            print(f"{AuthScope.SpreadSheet.value} not in auth. scopes:\n"
                  f"{self.auth_scopes}")
            return False

        # True if grid data should be returned.
        # This parameter is ignored if a field mask was set in the request.
        include_grid_data = False  # TODO: Update placeholder value.
        service = discovery.build('sheets', 'v4', credentials=self.authorized_creds)

        request = service.spreadsheets().get(spreadsheetId=self.spreadsheet_id,
                                             includeGridData=include_grid_data)
        response = request.execute()

        return response

    def get_sheets_properties(self) -> List[dict]:
        """Returns: A list of all sheets with their properties: sheetId,title,index..."""
        sheets = self.get_sheet_desc().get("sheets")
        sheet_properties = [sheet_property.get('properties') for sheet_property in sheets]
        return sheet_properties

    def read_gsheet(self,
                    sheet_name: str,
                    sheet_range: str,
                    as_dataframe: bool = True) -> Union[List[List], pd.DataFrame, None]:

        range_values: Union[List[List], pd.DataFrame, None] = None
        # check that we are requesting a GSheet Auth
        if not any(scope.value in self.auth_scopes for scope in [AuthScope.SpreadSheet, AuthScope.SpreadSheetReadOnly]):
            print(f"{AuthScope.SpreadSheet.value} or {AuthScope.SpreadSheetReadOnly.value} not in auth. scopes:\n"
                  f"{self.auth_scopes}")
            return range_values

        # The ranges to retrieve from the spreadsheet.
        sheet_range_addresses = f"{sheet_name}!{sheet_range}"

        try:
            service = discovery.build('sheets', 'v4', credentials=self.authorized_creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                        range=sheet_range_addresses).execute()
            range_values = result.get('values', [])

            if not range_values:
                print('No data found.')
                if as_dataframe:
                    return pd.DataFrame()
                else:
                    return []

        except HttpError as err:
            print(err)
            return range_values

        if as_dataframe:
            range_values = pd.DataFrame(data=range_values)

        return range_values

    def update_gsheet(self,
                      sheet_name: str,
                      sheet_new_values: List[List],
                      sheet_range: Optional[str] = None,
                      sheet_start_cell: Optional[str] = None,
                      ) -> int:
        """Returns the number of cells updated"""
        # https://developers.google.com/sheets/api/guides/values

        # check that we have the rights to modify the GSheet
        if AuthScope.SpreadSheet.value not in self.auth_scopes:
            print(f"{AuthScope.SpreadSheet.value} not in auth. scopes:\n"
                  f"{self.auth_scopes}")
            return -1

        # set sheet_range_address
        if sheet_range is None and sheet_start_cell is None:
            print(f'sheet_range and sheet_start_cell can not be None at the same time')
            return -1
        elif sheet_start_cell is not None:
            sheet_range = build_sheet_range(range_values=sheet_new_values,
                                            start_cell=sheet_start_cell)

        # The ranges to retrieve from the spreadsheet.
        sheet_range_addresses = f"{sheet_name}!{sheet_range}"
        updated_cells: int = 0
        try:
            service = discovery.build('sheets', 'v4', credentials=self.authorized_creds)
            body = {
                'values': sheet_new_values
            }
            result = service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id, range=sheet_range_addresses,
                valueInputOption="USER_ENTERED", body=body
            ).execute()

            updated_cells = result.get('updatedCells')

        except HttpError as error:
            print(f"An error occurred: {error}")

        return updated_cells

    def clear_gsheet_range(self,
                           sheet_name: str,
                           sheet_range: Optional[str] = None,
                           ) -> Union[str, None]:
        """Clear a given range when given, if None, it will clear the whole sheet"""
        # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/clear

        # check that we have the rights to modify the GSheet
        if not any(scope.value in self.auth_scopes for scope in [AuthScope.SpreadSheet,
                                                                 AuthScope.Drive,
                                                                 AuthScope.DriveFile]):
            print(f"{AuthScope.SpreadSheet.value} or {AuthScope.SpreadSheetReadOnly.value} not in auth. scopes:\n"
                  f"{self.auth_scopes}")
            return None

        # The ranges to retrieve from the spreadsheet.
        if sheet_range is None:
            sheet_range_addresses = f"{sheet_name}"
        else:
            sheet_range_addresses = f"{sheet_name}!{sheet_range}"

        try:
            service = discovery.build('sheets', 'v4', credentials=self.authorized_creds)
            clear_values_request_body = {
                # TODO: Add desired entries to the request body.
            }

            request = service.spreadsheets().values().clear(spreadsheetId=self.spreadsheet_id,
                                                            range=sheet_range_addresses,
                                                            body=clear_values_request_body)
            response = request.execute()

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

        return response.get("clearedRange")

    def create_spreadsheet(self, spreadsheet_name: str) -> Union[str, None]:
        """Create a new spreadsheet in the root of your Cloud Drive"""
        # https://developers.google.com/sheets/api/guides/create#python

        # check that we have the rights to modify/Create the GSheet
        if not any(scope.value in self.auth_scopes for scope in [AuthScope.SpreadSheet,
                                                                 AuthScope.Drive,
                                                                 ]):
            print(f"{AuthScope.Drive.value} or {AuthScope.SpreadSheet.value} not in auth. scopes:\n"
                  f"{self.auth_scopes}")
            return None

        try:
            service = discovery.build('sheets', 'v4', credentials=self.authorized_creds)
            spreadsheet = {
                'properties': {
                    'title': spreadsheet_name
                }
            }
            spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                        fields="spreadsheetId") \
                .execute()
            print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
            return spreadsheet.get('spreadsheetId')
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def create_new_sheet(self, sheet_name: str) -> Union[Dict, None]:
        """Create a new sheet on your spreadsheet using its spreadsheet_id"""
        # check that we have the rights to modify/Create the GSheet
        if not any(scope.value in self.auth_scopes for scope in [AuthScope.SpreadSheet,
                                                                 ]):
            print(f"{AuthScope.SpreadSheet.value} not in auth. scopes:\n"
                  f"{self.auth_scopes}")
            return None

        try:
            service = discovery.build('sheets', 'v4', credentials=self.authorized_creds)
            request = {
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }
            # Create a batch update request containing the addSheet request
            batch_update_request = {
                'requests': [request]
            }

            # Execute the batch update request
            response = service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id, body=batch_update_request).execute()
            return response.get("replies")[0].get("addSheet").get("properties")
        except HttpError as error:

            print(f"An error occurred: {error}")

            return None

    def delete_sheet(self, sheet_name: Optional[str] = None, sheet_id: Optional[int] = -1) -> Union[Dict, None]:
        """Create a new sheet on your spreadsheet using its spreadsheet_id"""
        # check that we have the rights to modify/Create the GSheet
        if not any(scope.value in self.auth_scopes for scope in [AuthScope.SpreadSheet,
                                                                 ]):
            print(f"{AuthScope.SpreadSheet.value} not in auth. scopes:\n"
                  f"{self.auth_scopes}")
            return None

        # get sheet id
        if sheet_id == -1 and sheet_name is not None:
            spreadsheet_desc = self.get_sheets_properties()

            for sheet in spreadsheet_desc:
                if sheet.get("title").upper() == sheet_name.upper():
                    sheet_id = sheet.get("sheetId")
            if sheet_id == -1:
                print(f"Error {sheet_name} was not found in workbook sheets:\n"
                      f"{spreadsheet_desc}")
                return None

        # Create a DeleteSheetRequest object
        delete_request = {
            "deleteSheet": {
                "sheetId": sheet_id
            }
        }

        # Create a batch update request
        batch_update_request = {
            "requests": [delete_request]
        }

        try:
            # Execute the batch update request to delete the sheet
            service = discovery.build('sheets', 'v4', credentials=self.authorized_creds)

            response = service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id, body=batch_update_request).execute()

            print('Sheet deleted successfully!')
            return response

        except HttpError as error:
            print(f'An error occurred: {error}')
            return None


if __name__ == '__main__':
    gsheet = GSheetHandler(auth_scopes=[AuthScope.Drive, AuthScope.SpreadSheet, AuthScope.SpreadSheetReadOnly],
                           spreadsheet_id=None)
    my_result = gsheet.delete_sheet(sheet_name="Sheet5")
    pprint(my_result)
