import argparse
import os

from urllib.request import urlretrieve
from pathlib import Path

DATA_DIR = 'data'
FILENAME = 'data.csv'
URL = 'https://raw.githubusercontent.com/tensorflow/tfx/master/tfx/examples/chicago_taxi_pipeline/data/simple/data.csv'


def main(uri):
    data_path = Path(uri)
    urlretrieve(URL, data_path.as_posix())
    print("データの書き込み場所: {}".format(data_path))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uri',  required=True)
    args = parser.parse_args()
    main(args.uri)
