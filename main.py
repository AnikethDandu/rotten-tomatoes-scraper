"""
Rotten Tomatoes Scraper

This script is a CLI tool that allows users to get top movies filtered by date,
year, and genre from the Rotten Tomatoes website:
(https://www.rottentomatoes.com).

This script requires that 'bs4' be installed within the Python environment you
are running this script in.

FUNCTIONS:
    - return_beautiful_soup_object(str) -> bs4.BeautifulSoup
    - return_movie_list(str) -> (bs4.element.NavigableString, list, list)

CONSTANTS:
    - MOVIE_GENRES
        - type: list
        - string list of all Rotten Tomatoes movie genres
    - ORIGINAL_GENRE
        - type: None, list
        - original genre specified by user. Can be None to represent Top 100
        Movies. Can be list with specific genre string(s)

VARIABLES:
    - base_url
        - type: str
        - generic Rotten Tomatoes Top 100 URL
    - parser
        - type: argparse.ArgumentParser
        - argparse ArgumentParser object to which arguments are added
    - args
        - type: argparse.Namespace
        - variables entered through arguments
"""

__docformat__ = 'reStructuredText'

import argparse
import bs4
from bs4 import BeautifulSoup
import urllib.request

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
base_url = 'https://www.rottentomatoes.com/top/bestofrt/'


def return_beautiful_soup_object(url: str) -> bs4.BeautifulSoup:
    """
    Returns BeautifulSoup object from HTML parsed from parameter url

    Grabs HTML and headers from parameter url. Opens HTML as a file and parses
    contents into BeautifulSoup object. Closes file and returns object.

    :param url: desired webpage url
    :type url: str
    :return: BeautifulSoup object from HTML parsed from parameter url
    :rtype: bs4.BeautifulSoup
    """
    html_filename, headers = urllib.request.urlretrieve(url)
    with open(html_filename) as file:
        soup = BeautifulSoup(file, 'html.parser')
        file.close()
    return soup


def return_movie_list(url: str) -> (bs4.element.NavigableString, list, list):
    """
    Returns title of top 100 movie list, top 100 movies, corresponding rotten
    tomato ratings

    Creates a BeautifulSoup object from parameter url. Creates list of table
    cells. Grabs list of ratings from span tags in cells. Grabs list of movies
    from cells. Returns tuple of BeautifulSoup object title, list of top 100
    movies, list of corresponding ratings.

    :param url: desired webpage url
    :type url: str
    :return: tuple of BeautifulSoup object title, list of top 100 movies, list
    of corresponding ratings
    :rtype: tuple
    """
    soup = return_beautiful_soup_object(url)
    cell_data_list = soup.find('body').find('div', {'class': 'col-left-center'}).find('table').find_all('td')
    span_rating_list = list([cell.find_all('span', {'class': 'tMeterScore'}) for cell in cell_data_list])
    rating_list = list([span[0].text.strip() for span in span_rating_list if span != []])
    movies = list(movie[0].text.strip() for movie in list([cell.find_all('a') for cell in cell_data_list])
                  if movie != [])
    return soup.title.contents[0], movies, rating_list


"""
Create ArgumentParser object, add arguments for length of movie list, genre, 
and year.
"""
parser = argparse.ArgumentParser(description='Return top movies from Rotten Tomatoes site')
parser.add_argument('-l', '--length', type=int, nargs='?', default=10,
                    help='Specify length of list of movies returned. Must at most 100')
parser.add_argument('-g', '--genre', type=str, nargs='*', default=None,
                    help=f'Select movie genre from following: {", ".join(list([movie for movie in MOVIE_GENRES]))}.'
                         ' For genres of multiple words, type each word of genre with space in between')
parser.add_argument('-y', '--year', type=int, nargs='?', default=None,
                    help='Choose year to view top [l] movies (cannot be used to find genre in specific year')
"""
Create object for variables from arguments. Store genre in separate variable. 
Check if genre is not None. If so, genre must be multi-word so combine words 
and store in object.
"""
args = parser.parse_args()
ORIGINAL_GENRE = args.genre
if args.genre is not None:
    args.genre = ' & '.join(args.genre)

"""
Check if user specified between 0 and 100 movies. Exit program if not.
"""
if not 0 < args.length <= 100:
    print('Please specify a number of movies from 1-100')
    exit()

"""
Check if genre is not None and is not valid genre in list. Exit program if so.
"""
if args.genre not in MOVIE_GENRES and args.genre is not None:
    print(f'{args.genre} is not a valid genre. '
          f'Please select one of the following: '
          f'{", ".join(list([movie for movie in MOVIE_GENRES]))}. '
          'For genres of multiple words, type each word of genre with space in between')
    exit()

"""
Check if no year specified
"""
if args.year is None:
    """
    If no year specified, check if no genre specified. If so, do not change url
    and use all-time top 100 list. If genre specified, add specific genre to 
    end of url to visit genre-specific webpage.
    """
    if args.genre is not None:
        base_url += 'top_100_' + \
                    '__'.join(list([word.strip().lower() for word in ORIGINAL_GENRE])) + '_movies/'
else:
    """
    If year specified, check if genre specified. If so, user has selected both 
    year and genre, exit program. If no genre specified, add year to url to
    visit top 100 movies in given year webpage.
    """
    if args.genre is not None:
        print('You cannot select a year and a genre. Please select only one')
        exit()
    else:
        base_url += f'?year={args.year}'

"""
Grab list title, movie list, and ratings list from url. Print title, movies 
with corresponding ratings in ranked list for [length] movies where length is 
variable user enters as optional argument.
"""
movie_category, top_movies, rtn_tomato_ratings = return_movie_list(base_url)
print(movie_category)
for i in range(args.length):
    print(f'{i + 1}. {top_movies[i]}: {rtn_tomato_ratings[i]}')
