import argparse
from bs4 import BeautifulSoup
import urllib

MOVIE_GENRES = [
    'Action & Adventure',
    'Animation',
    'Art house & International',
    'Classics',
    'Comedy',
    'Drama',
    'Kids & Family',
    'Musical & Performing Arts',
    'Mystery & Suspense',
    'Romance',
    'Science Fiction & Fantasy',
    'Special Interest',
    'Sports & Fitness',
    'Television',
    'Western',
]

parser = argparse.ArgumentParser(description='Return top movies from Rotten Tomatoes site')
parser.add_argument('-l', '--length', type=int, nargs='?', default=10)
parser.add_argument('-g', '--genre', type=str, nargs='?', default=None,
                    help=f'Movie genres: {", ".join(list([movie for movie in MOVIE_GENRES]))}')
parser.add_argument('-y', '--year', type=int, nargs='?', default=2020)
args = parser.parse_args()

if args.genre not in MOVIE_GENRES and args.genre is not None:
    print(f'{args.genre} is not a valid genre. '
          f'Please select one of the following:\n'
          f'{", ".join(list([movie for movie in MOVIE_GENRES]))}')
    exit()
