import os
import numpy as np
from optparse import OptionParser
import pandas as pd

CSV_FILENAME = 'lot_flight_position_labels.csv'
IMAGE_PATH_KEY = 'image_path'
IS_LOT_KEY = 'is_lot'


def load_dataframe():
    if os.path.exists(CSV_FILENAME):
        df = pd.read_csv(CSV_FILENAME, sep=',')
        return df
    else:
        print('ERROR: csv file '+CSV_FILENAME+' not found.')
        exit(0)
        return None


def print_valid_rows(df):
    valid = df.loc[df[IS_LOT_KEY].isin([0.0, 1.0, 0, 1])]
    num_valid = len(valid)
    print(' -> '+str(num_valid)+' Valid Rows of '+str(len(df)))
    return num_valid


def print_class_info(df, total_valid):
    is_lot = len(df.loc[df[IS_LOT_KEY].isin([1.0, 1])])
    not_lot = len(df.loc[df[IS_LOT_KEY].isin([0.0, 0])])

    r_is_lot = float(is_lot)/float(total_valid)
    r_not_lot = float(not_lot) / float(total_valid)

    print(' -> '+str(is_lot)+' ('+str(r_is_lot)+') are lot.')
    print(' -> '+str(not_lot)+' ('+str(r_not_lot)+') are not lot.')


def main():
    df = load_dataframe()
    valid = print_valid_rows(df)
    print_class_info(df, total_valid=valid)


if __name__ == "__main__":
    main()
