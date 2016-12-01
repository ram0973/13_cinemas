import argparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from lxml import etree

AFISHA_FILMS_URL = 'http://www.afisha.ru/msk/schedule_cinema/'
KINOPOISK_SEARCH = 'https://m.kinopoisk.ru/search/%s'
KINOPOISK_XML = 'https://rating.kinopoisk.ru/%s.xml'
MOVIES_COUNT = 20
CINEMAS_COUNT = 1


def fetch_html(url):
    return requests.get(url).content


def parse_afisha_list(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    titles = [tag.get_text() for tag in soup.select('h3.usetags a')]
    cinemas = [len(tags.select('td.b-td-item')) for tags in
               soup.select('div.s-votes-hover-area')]
    return [{'title': title, 'cinemas': cinemas_count}
            for title, cinemas_count in zip(titles, cinemas)]


def fetch_movie_info(movie_title):
    soup = BeautifulSoup(fetch_html(KINOPOISK_SEARCH % movie_title), 'lxml')
    try:
        film_url = soup.select('div.search')[0].select('a')[0].get('href')
        film_id = film_url.strip('/').split('/')[-1]

        tree = etree.XML(fetch_html(KINOPOISK_XML % film_id))
        rating = float(tree[0].text)
        votes = int(tree[0].get('num_vote'))
    except (IndexError, ValueError):
        rating = .0
        votes = 0
    return {'rating': rating, 'votes': votes}


def sort_by_rating(film):
    return film['rating']


def output_movies_to_console(movies_info):
    print('{:55}{:^9}{:^7}{:^9}'.format(
        'Title:', 'Cinemas', 'Rating', 'Votes'))
    for movie in movies_info:
        print('{:55}{:^9}{:^7}{:^9}'.format(
            movie['title'], movie['cinemas'], movie['rating'], movie['votes']))


def get_console_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--movies', '--m', help='Movies count',
                        default=MOVIES_COUNT, type=int)
    parser.add_argument('--cinemas', '--c', help='Cinemas count',
                        default=CINEMAS_COUNT, type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_console_args()

    print('Fetching movies and cinemas')
    titles_and_cinemas = parse_afisha_list(fetch_html(AFISHA_FILMS_URL))
    filtered_titles_and_cinemas = [item for item in titles_and_cinemas
                                   if int(item['cinemas']) >= args.cinemas]

    print('Fetching ratings and votes')
    movies = []
    for title_and_cinemas in tqdm(filtered_titles_and_cinemas):
        rating_and_votes = fetch_movie_info(title_and_cinemas['title'])
        movies.append({**title_and_cinemas, **rating_and_votes})
    movies.sort(key=sort_by_rating, reverse=True)

    print('\nBest %i movies, screening in at least %i cinemas' %
          (args.movies, args.cinemas))
    output_movies_to_console(movies[:args.movies])
