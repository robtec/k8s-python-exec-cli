import argparse
from os.path import exists


def file_exists(args):
    if not exists(args.file):
        print("file %s not found, exiting." % args.file)
        exit(1)


def process_file(args):
    data_file = open(args.file, 'r')
    lines_in_file = data_file.readlines()

    found = {}

    for line in lines_in_file:
        if 'hello' in line:
            parts = line.split('-')
            found[parts[0]] = parts[1]

    print(found)


def main():

    parser = argparse.ArgumentParser(description="Validate pvc data")
    parser.add_argument("--file", type=str, help="file to validate", required=True)

    args = parser.parse_args()

    file_exists(args)

    process_file(args)


if __name__ == '__main__':
    main()
