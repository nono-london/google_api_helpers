import pandas as pd

from google_api_helpers.g_sheet_helpers import (GSheetHandler, AuthScope)


def test_reader():
    gsheet = GSheetHandler(auth_scopes=[AuthScope.SpreadSheet])
    sheet_range = 'A1:G10'
    sheet_name = "Sheet1"

    result = gsheet.read_gsheet(sheet_name=sheet_name,
                                sheet_range=sheet_range,
                                as_dataframe=False)
    assert isinstance(result, list)


def test_reader_as_dataframe():
    gsheet = GSheetHandler(auth_scopes=[AuthScope.SpreadSheet])
    sheet_range = 'A1:G10'
    sheet_name = "Sheet1"

    result = gsheet.read_gsheet(sheet_name=sheet_name,
                                sheet_range=sheet_range,
                                as_dataframe=True)
    assert isinstance(result, pd.DataFrame)


def test_desc():
    gsheet = GSheetHandler(auth_scopes=[AuthScope.SpreadSheet])

    result = gsheet.get_sheet_desc()
    assert len(result.get("properties").get('title')) > 0


def test_sheet_properties():
    gsheet = GSheetHandler(auth_scopes=[AuthScope.SpreadSheet])

    result = gsheet.get_sheets_properties()
    assert len(result) > 0


if __name__ == '__main__':
    test_reader()
    test_reader_as_dataframe()
    test_desc()
    test_sheet_properties()
