import os
import numpy as np
from optparse import OptionParser
import pandas as pd
import cv2
import shutil


ORIGIN_CSV = 'lot_flight_position_labels.csv'
IMAGE_PATH_KEY = 'image_path'
IS_LOT_KEY = 'is_lot'

DEST_CSV = 'path_and_labels.csv'
ROOT_DIR = 'IsLotDataset'
RELATIVE_IMG_DIR = 'images'
IMG_DIR = ROOT_DIR+'/'+RELATIVE_IMG_DIR


def set_dirs():
    if os.path.isdir('./'+ROOT_DIR):
        print('Exists, deleting...')
        try:
            shutil.rmtree(IMG_DIR)
        except OSError:
            print("Deletion of the directory %s failed" % IMG_DIR)
        else:
            print("Successfully deleted the directory %s" % IMG_DIR)

    try:
        os.makedirs(IMG_DIR)
    except OSError:
        print("Creation of the directory %s failed" % IMG_DIR)
        exit(0)
    else:
        print("Successfully created the directory %s " % IMG_DIR)


def load_origin_dataframe():
    if os.path.exists(ORIGIN_CSV):
        df = pd.read_csv(ORIGIN_CSV, sep=',')
        df = df.loc[df[IS_LOT_KEY].isin([0.0, 1.0, 0, 1])]
        return df
    else:
        print('Could not load '+ORIGIN_CSV)
        exit(0)


def create_dest_dataframe():
    raw_data = {IMAGE_PATH_KEY: [],
                IS_LOT_KEY: []}
    df = pd.DataFrame(raw_data, columns=[IMAGE_PATH_KEY, IS_LOT_KEY])
    return df


def relative_dest_img_path_for(index):
    return RELATIVE_IMG_DIR+'/img_' + str(index) + '.jpg'


def dest_img_path_for(index):
    return ROOT_DIR+'/'+relative_dest_img_path_for(index)


def convert_image_in(origin_path, dest_path):
    img = cv2.imread(origin_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (480, 360))
    cv2.imwrite(filename=dest_path, img=img)


def populate_dest_dataframe(index, label, dataframe):
    relative_dest_path = relative_dest_img_path_for(index)
    return dataframe.append({IMAGE_PATH_KEY: relative_dest_path, IS_LOT_KEY: label}, ignore_index=True)


def store_destination_dataframe(df):
    df = df.astype({IS_LOT_KEY: int})
    df.to_csv(ROOT_DIR+'/'+DEST_CSV, sep=',', index=False)


def convert_dataset(origin, destination):
    for index, row in origin.iterrows():
        print(row[IMAGE_PATH_KEY], row[IS_LOT_KEY])
        path = row[IMAGE_PATH_KEY]
        label = row[IS_LOT_KEY]
        dest_path = dest_img_path_for(index)
        convert_image_in(path, dest_path=dest_path)
        destination = populate_dest_dataframe(index, label=label, dataframe=destination)
    store_destination_dataframe(destination)

def main():
    set_dirs()
    origin_df = load_origin_dataframe()
    dest_df = create_dest_dataframe()
    convert_dataset(origin_df, dest_df)


if __name__ == "__main__":
    main()
