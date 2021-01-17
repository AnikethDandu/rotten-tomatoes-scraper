import argparse
from bs4 import BeautifulSoup
import urllib.request

BASE_URL = 'https://www.rottentomatoes.com/top/bestofrt/'


def return_html_object(url):
    html_filename, headers = urllib.request.urlretrieve(url)
    with open(html_filename) as file:
        soup = BeautifulSoup(file, 'html.parser')
        file.close()
    return soup


def return_movie_list(url):
    soup = return_html_object(url)
    cell_data_list = soup.find('body').find('div', {'class': 'col-left-center'}).find('table').find_all('td')
    span_rating_list = list([cell.find_all('span', {'class': 'tMeterScore'}) for cell in cell_data_list])
    rating_list = list([span[0].text.strip() for span in span_rating_list if span != []])
    movies = list(movie[0].text.strip() for movie in list([cell.find_all('a') for cell in cell_data_list])
                  if movie != [])
    return soup.title.contents[0], movies, rating_list


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
parser.add_argument('-g', '--genre', type=str, nargs='*', default=None,
                    help=f'Select movie genre from following: {", ".join(list([movie for movie in MOVIE_GENRES]))}. '
                    'For genres of multiple words, type each word of genre with space in between')
parser.add_argument('-y', '--year', type=int, nargs='?', default=None,
                    help='Choose year to view top [l] movies (cannot be used to find genre in specific year')
args = parser.parse_args()
original_genre = args.genre
if args.genre is not None:
    args.genre = ' & '.join(args.genre)

if not 0 < args.length <= 100:
    print('Please specify a number of movies from 1-100')
    exit()

if args.genre not in MOVIE_GENRES and args.genre is not None:
    print(f'{args.genre} is not a valid genre. '
          f'Please select one of the following: '
          f'{", ".join(list([movie for movie in MOVIE_GENRES]))}. '
          'For genres of multiple words, type each word of genre with space in between')
    exit()

if args.year is None:
    if args.genre is not None:
        BASE_URL += 'top_100_' + \
                    '__'.join(list([word.strip().lower() for word in original_genre])) + '_movies/'
else:
    if args.genre is not None:
        print('You cannot select a year and a genre. Please select only one')
        exit()
    else:
        BASE_URL += f'?year={args.year}'
movie_category, top_movies, rtn_tomato_ratings = return_movie_list(BASE_URL)
print(movie_category)
for i in range(args.length):
    print(f'{i+1}. {top_movies[i]}: {rtn_tomato_ratings[i]}')
