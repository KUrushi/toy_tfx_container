import argparse

from urllib.request import urlretrieve
from pathlib import Path

DATA_DIR = 'data'
FILENAME = 'data.csv'
URL = 'https://raw.githubusercontent.com/tensorflow/tfx/master/tfx/examples/chicago_taxi_pipeline/data/simple/data.csv'


def main(uri):
    data_path = Path(uri)
    parent = data_path.parent
    if not parent.exists():
        parent.mkdir()

    urlretrieve(URL, data_path.as_posix())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uri',  required=True)
    args, _ = parser.parse_args()
    main(args.uri)
