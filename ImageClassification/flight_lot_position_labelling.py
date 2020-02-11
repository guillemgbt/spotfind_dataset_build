import os
import numpy as np
from optparse import OptionParser
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


parser = OptionParser()
parser.add_option("-p", "--path",
                  dest="image_root",
                  help="Path to look for images in subdirectories.")


(options, args) = parser.parse_args()

if not options.image_root:
    parser.error('Error: path to images must be specified. Pass --path to command line')

IMAGE_ROOT = options.image_root
CSV_FILENAME = 'lot_flight_position_labels.csv'
IMAGE_PATH_KEY = 'image_path'
IS_LOT_KEY = 'is_lot'


def load_image_paths():
    print('--> Looking for images in: ' + IMAGE_ROOT)

    images = []

    for root, dirs, files in os.walk(IMAGE_ROOT):
        for i, file in enumerate(files):
            if file.endswith(".jpg"):
                aux_root = root
                if not root.endswith("/"):
                    aux_root = aux_root + '/'
                images.append(aux_root + file)

    return images


def load_or_create_dataframe():
    if os.path.exists(CSV_FILENAME):
        df = pd.read_csv(CSV_FILENAME, sep=',')
        return df
    else:
        raw_data = {IMAGE_PATH_KEY: [],
                    IS_LOT_KEY: []}
        df = pd.DataFrame(raw_data, columns=[IMAGE_PATH_KEY, IS_LOT_KEY])
        return df


def filter_unlabelled_images(df, images):
    labelled_images = df[IMAGE_PATH_KEY].to_list()
    filtered_images = [item for item in images if item not in labelled_images]
    return filtered_images


def display_and_label(images):
    plt.ion()

    for i, image_path in enumerate(images):
        img = mpimg.imread(image_path)
        plt.imshow(img)
        plt.pause(0.05)
        label = input('is lot: ')
        store_observation(image=image_path, label=label)
        print('-> image:'+image_path+', is lot: '+str(label))
        print('-> '+str(i+1)+' of '+str(len(images))+' completed.')


def store_observation(image, label):
    df = load_or_create_dataframe()
    df = df.append({IMAGE_PATH_KEY: image, IS_LOT_KEY: label}, ignore_index=True)
    df.to_csv(CSV_FILENAME, sep=',', index=False)


def main():
    images = load_image_paths()
    df = load_or_create_dataframe()
    images = filter_unlabelled_images(df=df, images=images)
    display_and_label(images)


if __name__ == "__main__":
    main()
