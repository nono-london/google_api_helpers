from google_api_helpers.misc_helpers import (build_sheet_range, a2n, n2a)


def test_letter_to_column_number():
    assert a2n("BD") == 56


def test_column_number_to_letter():
    assert n2a(56) == "BD"


def test_build_sheet_range():
    values = [['A', 'B'],
              ['C', 'D'],
              ['E', 'F']
              ]
    result = build_sheet_range(start_cell="b10", range_values=values)
    assert result == "B10:C12"


if __name__ == '__main__':
    test_letter_to_column_number()
    test_column_number_to_letter()
    test_build_sheet_range()
