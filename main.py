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
parser.add_argument('-l', '--length', type=int, nargs='?', default=10,
                    help='Specify length of list of movies returned. Must at most 100')
parser.add_argument('-g', '--genre', type=str, nargs='?', default=None,
                    help=f'Select movie genre from following: {", ".join(list([movie for movie in MOVIE_GENRES]))}')
parser.add_argument('-y', '--year', type=int, nargs='?', default=None,
                    help='Choose year to view top [l] movies (cannot be used to find genre in specific year')
args = parser.parse_args()

if not 0 < args.length <= 100:
    print('Please specify a number of movies from 1-100')
    exit()

if args.genre not in MOVIE_GENRES and args.genre is not None:
    print(f'{args.genre} is not a valid genre. '
          f'Please select one of the following:\n'
          f'{", ".join(list([movie for movie in MOVIE_GENRES]))}')
    exit()

if args.year is not None and args.genre is not None:
    print('You cannot select a year and a genre. Please select only one')
    exit()
