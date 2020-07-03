import argparse

import xgboost

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--example', nargs="+", required=True)
    args, _ = parser.parse_args()
    print(args.example)