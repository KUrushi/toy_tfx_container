from urllib.request import urlretrieve
from pathlib import Path

DATA_DIR = 'data'
FILENAME = 'data.csv'
URL = 'https://raw.githubusercontent.com/tensorflow/tfx/master/tfx/examples/chicago_taxi_pipeline/data/simple/data.csv'


def main():
    data_path = Path(__file__) / DATA_DIR
    filename = data_path / FILENAME
    if not data_path.exists():
        data_path.mkdir()

    urlretrieve(URL, filename)


if __name__ == "__main__":
    main()
