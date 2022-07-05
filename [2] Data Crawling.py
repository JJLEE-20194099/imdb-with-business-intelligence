import os
from src.text_csv_utils import write_csv_file, read_text_file
from src.yaml_utils import read_yaml
from src.url_functions import get_all_movie_ids_from_genre, get_user_id_list_rating_a_movie, get_detail_movie_by_movie_id, get_all_ratings_by_user, get_rating_list_in_a_movie, get_detail_movie_by_movie_id


ID_OUTPUT = 'data/crawl_data/movie_id'
os.makedirs(ID_OUTPUT, exist_ok=False)

MOVIE_IDS_PATH = './data/datasets/movie/ids.txt'

# 1. Craw movie_ids -> distribute them in ./data/crawl_data/movie_id
def crawl_movie_ids():

    links = read_yaml("./src/links/genre_links.yaml")
    for genre, links in links.items():

        genre_dir = os.path.join(ID_OUTPUT, genre)
        os.makedirs(genre_dir, exist_ok=False)

        item_id_list_path = os.path.join(genre_dir, 'id_list.txt')
        item_id_list = get_all_movie_ids_from_genre(links)
        write_csv_file(item_id_list, item_id_list_path, 'w')
            
# crawl_movie_ids() 
# ------------------------------------------------------------------

# 2. Combine movie ids -> distribute them in ./data/datasets/movie/ids.txt
def combine_movie_ids_from_category_dir():
    
    links = read_yaml("./src/links/genre_links.yaml")
    
    distinct_movie_ids = set()
    for genre, links in links.items():
        
        genre_dir = os.path.join(ID_OUTPUT, genre)
        item_id_list_path = os.path.join(genre_dir, 'id_list.txt')
        id_file = open(item_id_list_path, 'r')
        ids = id_file.readlines()
        for id in ids:
            distinct_movie_ids.add(id.strip())
    
    distinct_movie_ids = list(distinct_movie_ids)
    distinct_movie_ids = [[movie_id] for movie_id in distinct_movie_ids]

    movie_ids_path = os.path.join('data/datasets/movie/', 'ids.txt')
    write_csv_file(distinct_movie_ids, movie_ids_path, 'w')
    
# combine_movie_ids_from_category_dir()
# --------------------------------------------------------------------

# 3. Crawl movie details from all movie ids -> distribute them in ./data/datasets/movie/details.csv
def crawl_movie_details():
    movie_id_file = open(MOVIE_IDS_PATH, 'r')
    movie_id_file = movie_id_file.readlines()
    movie_id_file = [movie_id.strip() for movie_id in movie_id_file]
    movie_detail_path = os.path.join('data/datasets/movie', 'details.csv')
    
    detail_title = ["movie id", "title", "series", "release year", "certification", "duration", "average rating", "rating total", "genre list", "content", "countries of origin", "official sites", "languages", "production companies", "budget"]
    write_csv_file([detail_title], movie_detail_path, 'w')

    for movie_id in movie_id_file:
        write_csv_file([get_detail_movie_by_movie_id(movie_id)], movie_detail_path, 'a')
                
# crawl_movie_details()
# --------------------------------------------------------------------

# 4. Crawl user ids by finding user ids appear in rating box
def crawl_user_ids():
    movie_id_file = open(MOVIE_IDS_PATH, 'r')
    movie_ids = movie_id_file.readlines()
    
    USER_OUTPUT = 'data/datasets/user'
    os.makedirs(USER_OUTPUT, exist_ok=False)
    user_id_list_path = os.path.join(USER_OUTPUT, "fake_ids.txt")

    for movie_id in movie_ids:
        user_id_list = get_user_id_list_rating_a_movie(movie_id.strip())
        write_csv_file(user_id_list, user_id_list_path, 'a')

# crawl_user_ids()
# --------------------------------------------------------------------

# 5. Crawl ratings by finding contents in rating box
def crawl_rating_list():
    movie_id_file = open(MOVIE_IDS_PATH, 'r')
    movie_ids = movie_id_file.readlines()
    
    RATING_OUTPUT = 'data/datasets/rating'
    os.makedirs(RATING_OUTPUT, exist_ok=False)
    rating_list_path = os.path.join(RATING_OUTPUT, "details.csv")
    rating_title = ["user id", "movie id", "rating", "content", "date"]
    write_csv_file([rating_title], rating_list_path, 'w')
    for movie_id in movie_ids:
        rating_list = get_rating_list_in_a_movie(movie_id.strip())
        write_csv_file(rating_list, rating_list_path, 'a')

# crawl_rating_list()
# --------------------------------------------------------------------

# 6. Crawl more ratings by getting ratings of each user
def crawl_rating_by_all_users():
    user_id_file = open('./data/datasets/user/fake_ids.txt', 'r')
    user_ids = user_id_file.readlines()

    RATING_OUTPUT = 'data/datasets/rating'
    os.makedirs(RATING_OUTPUT, exist_ok=False)

    rating_list_path = os.path.join(RATING_OUTPUT, 'all_details.csv')
    rating_title = ["user id", "movie id", "rating", "timestamp"]
    write_csv_file([rating_title], rating_list_path, 'w')
    for user_id in user_ids:
        write_csv_file(get_all_ratings_by_user(user_id.strip()), rating_list_path, 'a')

# unnecessary 
# crawl_rating_by_all_users() 
# --------------------------------------------------------------------

