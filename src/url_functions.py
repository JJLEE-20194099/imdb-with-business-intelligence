from bs4 import BeautifulSoup
import requests
from src.exception_utils import get_text, get_href, get_value_by_idx_list, get_a_children_by_find, get_a_children_by_find_class, get_childrens_by_find, get_childrens_by_find_class, get_len, get_childrens_by_find_no_recursive

def get_content_(url):
    """
    Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Encoding:gzip, deflate, sdch
    Accept-Language:en-US,en;q=0.8,vi;q=0.6
    Connection:keep-alive
    Cookie:__ltmc=225808911; __ltmb=225808911.202893004; __ltma=225808911.202893004.204252493; _gat=1; __RC=4; __R=1; _ga=GA1.3.938565844.1476219934; __IP=20217561; __UF=-1; __uif=__ui%3A-1%7C__uid%3A877575904920217840%7C__create%3A1475759049; __tb=0; _a3rd1467367343=0-9
    Host:dantri.com.vn
    Referer:http://dantri.com.vn/su-kien.htm
    Upgrade-Insecure-Requests:1
    User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36
    """
    headers = dict()
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Encoding'] = 'gzip, deflate, sdch'
    headers['Accept-Language'] = 'en-US,en;q=0.8,vi;q=0.6'
    headers['Connection'] = 'keep-alive'
    headers['Upgrade-Insecure-Requests'] = '1'
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    r = requests.get(url, headers=headers, timeout=10)
    r.encoding = 'utf-8'
    r.close()
    return str(r.text)

def get_all_film_links_from_a_imdb_another_url(url):
    try:
        raw_content = get_content_(url)
        soup = BeautifulSoup(raw_content, "html.parser")
        title_columns = soup.find_all("td", class_="titleColumn")
        links = []
        for title_column in title_columns:
            url = get_a_children_by_find(title_column, "a")
            links.append(get_value_by_idx_list(url, "href"))
        
        return links
    except Exception:
        return None


def generate_imdb_genre_links_from_base_genre_url(url, pagination_idx):
    genre_links = []
    current_start = 1
    for i in range(800):
        genre_links.append(url.format(current_start))
        current_start += pagination_idx
    return genre_links
    
def get_all_film_links_from_a_imdb_genre_url(url):
    try:
        raw_content = get_content_(url)
        soup = BeautifulSoup(raw_content, "html.parser")
        lister_item_header =  get_childrens_by_find_class(soup, "h3", "lister-item-header")
        links = []
        for item_header in lister_item_header:
            url = get_a_children_by_find(item_header, "a")
            links.append(get_value_by_idx_list(url, "href"))
        
        return links
    except Exception:
        return None

def get_id_from_a_film_link(url):
    try:
        return url.split("/")[2] 
    except Exception:
        return None
def get_id_from_a_user_link(url):
    try:
        return url.split("/")[2]
    except Exception:
        return None

def get_all_movie_ids_from_genre(links_per_genre):
    res = []
    for link in links_per_genre:
        all_list_urls_by_genre = generate_imdb_genre_links_from_base_genre_url(link, 50)
        for list_url in all_list_urls_by_genre:
            all_film_links_by_url = get_all_film_links_from_a_imdb_genre_url(list_url)
            for film_link in all_film_links_by_url:
                res.append([get_id_from_a_film_link(film_link)])
    return res



def get_ratings_by_a_user_follow_url(user_id, start):
    try:
        rating_url = 'https://www.imdb.com/user/{}/ratings?lastPosition={}'.format(user_id, start)
        
        raw_content = get_content_(rating_url)
        soup = BeautifulSoup(raw_content, "html.parser")
        
        lister_item_content = get_childrens_by_find_class(soup, "div", "lister-item-content")
        print(len(lister_item_content))
        data = []
        for item_content in lister_item_content:
            
            item_header = get_a_children_by_find_class(item_content, "h3", "lister-item-header")
            url = get_a_children_by_find(item_header, "a")
            movie_id = get_id_from_a_film_link(get_value_by_idx_list(url, "href"))
            ipl_rating_widget =  get_a_children_by_find_class(item_content, "div", "ipl-rating-widget")
            ratings =  get_childrens_by_find_class(ipl_rating_widget, "span", "ipl-rating-star__rating")
            rating_time = ipl_rating_widget.find_next_sibling("p")
            data.append([user_id, movie_id, get_text(get_value_by_idx_list(ratings, 1)), get_text(rating_time)])
        return data
    except Exception:
        return None

def get_all_ratings_by_user(user_id):
    curr_start = 0
    res = []
    res = get_ratings_by_a_user_follow_url(user_id, curr_start)
    # curr_start = 100
    # for i in range(1):
    #     res.extend(get_ratings_by_a_user_follow_url(user_id, curr_start))
    #     curr_start += 100
    return res


def get_user_id_list_rating_a_movie(movie_id):
    try:
        review_url = "https://www.imdb.com/title/{}/reviews".format(movie_id)
        raw_content = get_content_(review_url)
        soup = BeautifulSoup(raw_content, features="lxml")
        user_id_box_list =  get_childrens_by_find_class(soup, "span", "display-name-link")
        user_id_list = []
        for user_id_box in user_id_box_list[0:20]:
            url = get_a_children_by_find(user_id_box, "a")
            user_id = get_id_from_a_user_link(get_value_by_idx_list(url, "href"))
            user_id_list.append([user_id])
        
        return user_id_list
    except Exception:
        return None

def get_rating_list_in_a_movie(movie_id):
    try:
        review_url = "https://www.imdb.com/title/{}/reviews".format(movie_id)
        raw_content = get_content_(review_url)
        soup = BeautifulSoup(raw_content, features="lxml")
        rating_box_list = get_childrens_by_find_class(soup, "div", "lister-item-content")
        rating_list = []
        for rating_box in rating_box_list[0:20]:
            rating = []

            rating_scrore_box = get_a_children_by_find_class(rating_box, "span", "rating-other-user-rating")
            rating_score = get_text(get_a_children_by_find(rating_scrore_box, "span"))
            content_box = get_a_children_by_find_class(rating_box, "div", "content")
            content = get_text(get_a_children_by_find(content_box, "div"))

            name_date_box = get_a_children_by_find_class(rating_box, "div", "display-name-date")
            date = get_text(get_a_children_by_find_class(name_date_box, "span", "review-date"))
            url_box = get_a_children_by_find_class(name_date_box, "span", "display-name-link")
            url = get_a_children_by_find(url_box, "a")
            user_id = get_id_from_a_user_link(get_value_by_idx_list(url, "href"))
            

            rating.append(user_id)
            rating.append(movie_id)
            rating.append(rating_score)
            rating.append(content)
            rating.append(date)
            rating_list.append(rating)
        
        return rating_list
    except Exception:
        return None

res = []

def get_detail_movie_by_movie_id(movie_id):
    try:
        detail_url = "https://www.imdb.com/title/{}/".format(movie_id)
        raw_content = get_content_(detail_url)
        soup = BeautifulSoup(raw_content, features="lxml")

        title = get_text(soup.select_one('h1[data-testid="hero-title-block__title"]'))
        title_metadata_container = soup.select_one('ul[data-testid="hero-title-block__metadata"]')
        presentations =  get_childrens_by_find(title_metadata_container, "li")
        series = ""
        release_year = ""
        certification = ""
        duration = ""
        if get_len(presentations) == 4:
            series = presentations[0].get_text()
            release_year = get_text(get_a_children_by_find(presentations[1], "span"))
            certification = get_text(get_a_children_by_find(presentations[2], "span"))
            duration = get_text(presentations[3])
        else :
            
            if (get_len(presentations) > 0):
                release_year = get_text(get_a_children_by_find(presentations[0], "span"))
    
            if (get_len(presentations) > 1):
                certification = get_text(get_a_children_by_find(presentations[1], "span"))
    
            if (get_len(presentations) > 2):
                duration = get_text(presentations[2])

        average_rating_block_container = soup.select_one('div[data-testid="hero-rating-bar__aggregate-rating"]')
        average_rating = ""
        average_rating = get_text(get_a_children_by_find_class(average_rating_block_container, "span", "sc-7ab21ed2-1 jGRxWM"))
        total_rating = ""
        total_rating = get_text(get_a_children_by_find_class(average_rating_block_container, "div", "sc-7ab21ed2-3 dPVcnq"))


        popularity_score = get_text(soup.select_one('div[data-testid="hero-rating-bar__popularity__score"]'))
        popularity_delta = get_text(soup.select_one('div[data-testid="hero-rating-bar__popularity__delta"]'))
        
        

        
        genres_and_plot_content = soup.select_one('div[data-testid="genres"]')
        genres_box = get_childrens_by_find(get_value_by_idx_list(get_childrens_by_find(genres_and_plot_content, "div"), 1), "a")
        genre_list = []
        plot_content = ""

        plot_content = get_text(soup.select_one('span[data-testid="plot-l"]'))

        if genres_box:
            for genre_box in genres_box:
                genre_title = get_text(genre_box)
                if genre_title:
                    genre_list.append(genre_title)

        overall_review_info_container = get_childrens_by_find(soup.select_one('ul[data-testid="reviewContent-all-reviews"]'), "li")
        numOfUserReviews = get_text(get_a_children_by_find_class(get_value_by_idx_list(overall_review_info_container, 0), "span", "score"))
        numOfCriticReviews = get_text(get_a_children_by_find_class(get_value_by_idx_list(overall_review_info_container, 1), "span", "score"))
        metaScore = get_text(get_a_children_by_find_class(get_value_by_idx_list(overall_review_info_container, 2), "span", "score"))

        role_container_box = soup.select_one('div[data-testid="title-pc-wide-screen"]')
        try:
            role_container_list_box = get_a_children_by_find(role_container_box, "ul").find_all(recursive=False)
        except: 
            role_container_list_box = None
        star_container_box = get_childrens_by_find(get_a_children_by_find(get_value_by_idx_list(role_container_list_box, -1), "ul"), "li")
        star_url_list = []

        if star_container_box:
            for star_box in star_container_box:
                star_url = get_value_by_idx_list(get_a_children_by_find(star_box, "a"), "href")
                star_url_list.append(star_url)

        countries_of_origin = []
        official_sites = []
        languages = []
        filming_locations = []
        production_companies = []
        budget = ""
        
        countries_of_origin_container = soup.select_one('li[data-testid="title-details-origin"]')
        countries = get_childrens_by_find(countries_of_origin_container, "a")
        if countries:
            for country in countries:
                countries_of_origin.append(get_text(country))
        
        official_sites_container = soup.select_one('li[data-testid="details-officialsites"]')

        sites = get_childrens_by_find(official_sites_container, "a")
        if sites:
            for site in sites:  
                official_sites.append(get_text(site))
        
        languages_container = soup.select_one('li[data-testid="title-details-languages"]')
        
        langs = get_childrens_by_find(languages_container, "a")
        
        if langs:
            for lang in langs:
                languages.append(get_text(lang))   

        filming_location_container = soup.select_one('li[data-testid="title-details-filminglocations"]')

        locations = get_childrens_by_find(filming_location_container, "a")
        if locations:
            for location in locations:
                filming_locations.append(get_text(location))   
        companies_container = soup.select_one('li[data-testid="title-details-companies"]')

        companies = get_childrens_by_find(companies_container, "a")
        if companies:
            for company in companies:
                production_companies.append(get_text(company))
        
        budgets = get_childrens_by_find(get_a_children_by_find(soup.select_one('li[data-testid="title-boxoffice-budget"]'), "ul"), "li")
        # print(title, budgets, detail_url)

        budget_list = []
        if budgets:
            for budget in budgets:
                budget = get_text(budget)
                budget_list.append(budget)

        return [movie_id, title, series, release_year, certification, duration, average_rating, total_rating, popularity_score, popularity_delta, plot_content, numOfUserReviews, numOfCriticReviews, metaScore, "|".join(star_url_list), "|".join(countries_of_origin), "|".join(official_sites), "|".join(languages), "|".join(filming_locations), "|".join(production_companies), "|".join(budget_list)]

    except Exception:
        return None



    
