import argparse

import mmh3
import numpy as np

# argparser preliminaries
parser = argparse.ArgumentParser(description='Hash protein accession database')
parser.add_argument('-i', '--input_path', help='path to database')
parser.add_argument('-o', '--output_path', help='path where to save hashed database')
args = parser.parse_args()


def hash_database(input_path, output_path, seed=18):
    """
    Perform mmh3 hashing on input database.
    MurmurHash3 is a non-cryptographic hashing algorithm.
    For more information on mmh3 algorithm visit https://pypi.org/project/mmh3/.

    :param input_path: str, input path
    :param output_path: str, output path
    :param seed: int, hashing seed: use identical integer for identical hashing results
    :return: database: np.array, hashed database
    """
    # initialize database
    database = np.empty([sum(1 for _ in open(input_path))])
    # hash protein accessions
    with open(input_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            database[line_num - 1] = mmh3.hash64(line, signed=False, seed=seed)[0]
    # save in numpy format
    np.save(output_path, database)


hash_database(args.input_path, args.output_path)
