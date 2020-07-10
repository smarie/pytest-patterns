from collections import namedtuple
from pathlib import Path

import numpy as np
from pytest_cases import parametrize


Dataset = namedtuple("Dataset", ('x', 'y'))
"""A minimal structure representing a dataset"""


# ------------- example data created by scripts --------------
@parametrize(id=range(1, 5))
def data_anscombes_quartet(id):
    """ Generate one case for each of the Anscombe's quartet """
    if id == 1:
        x = [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]
        y = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
    elif id == 2:
        x = [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]
        y = [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]
    elif id == 3:
        x = [10.0, 8.0, 13.0, 9.0, 11.0, 14.0, 6.0, 4.0, 12.0, 7.0, 5.0]
        y = [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]
    elif id == 4:
        x = [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 19.0, 8.0, 8.0, 8.0]
        y = [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]
    else:
        raise ValueError("Anscombes quartet contains, well... 4 datasets. "
                         "Invalid i=%s" % id)

    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    return Dataset(x, y)


# -------------- example data created from files --------------
datasets_dir = Path(__file__).parent / 'datasets'
all_csv_files = [datasets_dir / file_name for file_name in datasets_dir.glob('*.csv')]


@parametrize(csv_file_path=all_csv_files, idgen=lambda csv_file_path: csv_file_path.stem)
def data_csvfile(csv_file_path):
    """ Generates one case per file in the datasets/ folder """
    my_data = np.genfromtxt(csv_file_path, delimiter=',', names=True)
    return Dataset(x=my_data['x'], y=my_data['y'])
