from google_api_helpers.g_sheet_helpers import (GSheetHandler, AuthScope)


def test_writer_with_range():
    gsheet = GSheetHandler(auth_scopes=[AuthScope.SpreadSheet],
                           spreadsheet_id=None)
    updated_rows = gsheet.update_gsheet(sheet_name="Sheet1",
                                        sheet_range="A1:B2",
                                        sheet_new_values=[['A', 'B'],
                                                          ['C', 'D']
                                                          ])
    assert updated_rows > 0


def test_writer_with_start_cell():
    gsheet = GSheetHandler(auth_scopes=[AuthScope.SpreadSheet],
                           spreadsheet_id=None)
    updated_rows = gsheet.update_gsheet(sheet_name="Sheet1",
                                        sheet_start_cell="b8",
                                        sheet_new_values=[['A', 'B'],
                                                          ['C', 'D']
                                                          ])
    assert updated_rows > 0


if __name__ == '__main__':
    test_writer_with_range()
    test_writer_with_start_cell()
