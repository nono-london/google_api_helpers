from google_api_helpers.g_sheet_helpers import (GSheetHandler, AuthScope)


def test_new_sheet():
    gsheet = GSheetHandler(auth_scopes=[AuthScope.SpreadSheet],
                           spreadsheet_id=None)
    spreadsheet = gsheet.create_new_sheet(sheet_name="TestSheet1",

                                          )
    assert spreadsheet is not None


def test_delete_sheet():
    gsheet = GSheetHandler(auth_scopes=[AuthScope.SpreadSheet],
                           spreadsheet_id=None)
    spreadsheet = gsheet.delete_sheet(sheet_name="TestSheet1",

                                      )
    assert spreadsheet is not None


if __name__ == '__main__':
    test_new_sheet()
    test_delete_sheet()
