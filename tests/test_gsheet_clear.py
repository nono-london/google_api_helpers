from google_api_helpers.g_sheet_helpers import (GSheetHandler, AuthScope)


def test_clear_range():
    gsheet = GSheetHandler(auth_scopes=[AuthScope.SpreadSheet],
                           spreadsheet_id=None)
    range_cleared = gsheet.clear_gsheet_range(sheet_name="Sheet1",
                                              sheet_range="A1:b5"
                                              )
    assert range_cleared is not None


def test_clear_all_cells():
    gsheet = GSheetHandler(auth_scopes=[AuthScope.SpreadSheet],
                           spreadsheet_id=None)
    range_cleared = gsheet.clear_gsheet_range(sheet_name="Sheet1",
                                              sheet_range=None
                                              )
    assert range_cleared is not None


if __name__ == '__main__':
    test_clear_range()
    test_clear_all_cells()
