import re
from typing import List

import numpy as np


def n2a(n):
    letters = ""
    while n > 0:
        n -= 1
        letters = chr(n % 26 + 65) + letters
        n //= 26
    return letters.upper()


def a2n(a):
    n = 0
    for c in a:
        n = n * 26 + (ord(c.upper()) - 64)
    return n


def build_sheet_range(range_values: List[List], start_cell: str = "A1", ):
    letter_start, row_start = re.findall(r'[a-zA-Z]+|\d+', start_cell)
    row_start = int(row_start)

    rows_n = np.array(range_values).shape[1]
    columns_n = np.array(range_values).shape[1]

    letter_end = n2a(a2n(letter_start) + columns_n - 1)
    sheet_range = (str(start_cell) + str(f":{letter_end}{rows_n + int(row_start)}")).upper()
    return sheet_range


if __name__ == '__main__':
    values = [['A', 'B'],
              ['C', 'D'],
              ['E', 'F']
              ]
    print(build_sheet_range(start_cell="b10", range_values=values))