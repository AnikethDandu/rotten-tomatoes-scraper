import argparse

parser = argparse.ArgumentParser(description='Return top movies from Rotten Tomatoes site')
parser.add_argument('--n', type=int, nargs='?', const='10', default='10')
args = parser.parse_args()
