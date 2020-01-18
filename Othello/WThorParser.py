import argparse

MASTER_PATH = './../Data/'

def extractBoardStates(filename):
    file_path = MASTER_PATH + filename + '.wtb'
    with open(file_path, 'rb') as games_file:
        game_data = games_file.read()
        header_data = game_data[:16]

        for byte in header_data:
            print(int(byte))

        number_of_records = header_data[4:8]

        print(int.from_bytes(number_of_records, 'little'))

    print()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse WThor files')
    parser.add_argument('Filename', metavar='F', type=str, help='The filename \
         of the .wtb file to be parsed')

    args = parser.parse_args()
    filename = args.Filename

    extractBoardStates(filename)

    