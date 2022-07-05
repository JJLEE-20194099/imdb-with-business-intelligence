from bs4 import BeautifulSoup
import requests
from src.exception_utils import get_text, get_href, get_value_by_idx_list, get_a_children_by_find, get_a_children_by_find_class, get_childrens_by_find, get_childrens_by_find_class, get_len

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
    for i in range(30):
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
        title_block_container =  get_a_children_by_find_class(soup, "div", "TitleBlock__Container-sc-1nlhx7j-0")
        title = ""
        title = get_text(get_a_children_by_find_class(title_block_container, "h1", "TitleHeader__TitleText-sc-1wu6n3d-0"))

        title_metadata_container =  get_a_children_by_find_class(title_block_container, "div", "TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2")
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
    
        
        average_rating = ""
        average_rating = get_text( get_a_children_by_find_class(title_block_container, "span", "AggregateRatingButton__RatingScore-sc-1ll29m0-1"))
        
        total_rating = ""
        get_a_children_by_find_class(title_block_container, "div", "AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3")
        total_rating = get_text(get_a_children_by_find_class(title_block_container, "div", "AggregateRatingButton__TotalRatingAmount-sc-1ll29m0-3"))

        
        about_movie_container = get_a_children_by_find_class(soup, "div", "Hero__ContentContainer-kvkd64-10")
        
        genres_and_plot_content = get_a_children_by_find_class(about_movie_container, "div", "GenresAndPlot__ContentParent-cum89p-8")
        
        genres_box = get_childrens_by_find(genres_and_plot_content, "a")
        genre_list = []
        plot_content = ""

        plot_content = get_text(get_a_children_by_find_class(genres_and_plot_content, "span", "GenresAndPlot__TextContainerBreakpointL-cum89p-1"))
        if genres_box:
            for genre_box in genres_box:
                genre_title = get_text(get_a_children_by_find(genre_box, "span"))
                if genre_title:
                    genre_list.append(genre_title)

        
        storyline_wrapper = get_a_children_by_find_class(soup, "div", "Storyline__StorylineWrapper-sc-1b58ttw-0")
        storyline_content = get_text(get_a_children_by_find(storyline_wrapper, "div"))

        countries_of_origin = []
        official_sites = []
        languages = []
        production_companies = []
        budget = ""
        
        countries_of_origin_container = soup.select_one('li[data-testid="title-details-origin"]')

        countries = get_childrens_by_find(countries_of_origin_container, "a")
        if countries:
            for country in countries:
                if country:
                    countries_of_origin.append(get_text(country))
        
        official_sites_container = soup.select_one('li[data-testid="title-details-officialsites"]')

        sites = get_childrens_by_find(official_sites_container, "a")
        if sites:
            for site in sites:
                if site:
                    official_sites.append(get_text(site))
        
        languages_container = soup.select_one('li[data-testid="title-details-languages"]')

        langs = get_childrens_by_find(languages_container, "a")
        
        if langs:
            for lang in langs:
                if lang:
                    languages.append(get_text(lang))   

        companies_container = soup.select_one('li[data-testid="title-details-companies"]')

        companies = get_childrens_by_find(companies_container, "a")
        if companies:
            for company in companies:
                if (production_companies):
                    production_companies.append(company.get_text())
        budgets = get_childrens_by_find(get_a_children_by_find_class(soup, "ul", "BoxOffice__MetaDataListBoxOffice-sc-40s2pl-0"), "li")
        budget = get_text(get_value_by_idx_list(budgets, -1))
                
        
        content = plot_content + ' ' + storyline_content

        return [movie_id, title, series, release_year, certification, duration, average_rating, total_rating, "|".join(genre_list), content, "|".join(countries_of_origin), "|".join(official_sites), "|".join(languages), "|".join(production_companies), budget]
    except Exception:
        return None



    
