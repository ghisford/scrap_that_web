# Find top movies on IMDB since 1980 using web scraping 
# and save the result in a csv file. The csv file should 
# have the following columns: title, year, rating, metascore,
#  votes, gross, director, actors, runtime, genre, description. 
#  The csv file should be sorted by rating in descending order.
#   The csv file should have the following columns: title, year,
#    rating, metascore, votes, gross, director, actors, runtime, 
#    genre, description. The csv file should be sorted by rating in descending order.

from bs4 import BeautifulSoup 
import requests
import csv

url = "https://www.imdb.com/chart/top"

response = requests.get(url)

html_doc = BeautifulSoup(response.content,'html.parser')

movies_page = html_doc.find('tbody',class_ = 'lister-list')
movies = movies_page.find_all('tr')
movies_found  ={}


def movie_details(url):
    for index,movie in enumerate(movies):

        movie_year = movie.find('span',class_ ="secondaryInfo")
        if movie_year == None:
            continue
        movie_year = int(str(movie_year.text)[1:-1])
        if movie_year >= 1980:
            
            rating = float(movie.find('td', class_ = "ratingColumn imdbRating").strong.text)
            movie_url = f"https://www.imdb.com{movie.find('td',class_ = 'titleColumn').find('a')['href']}"
            movie_page = requests.get(movie_url)
            movie_html = BeautifulSoup(movie_page.content,'html.parser')
            runtime = movie_html.find('div',class_ = 'sc-80d4314-2 iJtmbR').find_all('li',class_ = 'ipc-inline-list__item')[-1].text
            voters = movie_html.find('div',class_ = 'sc-7ab21ed2-3 dPVcnq').text
            director = movie_html.find('div',class_ = 'ipc-metadata-list-item__content-container').a.text
            genre = movie_html.find('a',class_  = 'sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt').text
            description = movie_html.find('span',class_ = 'sc-16ede01-0 fMPjMP').text
            actors = movie_html.find('div',"ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid").find_all('a')
            actor_names = [ actor.text for actor in actors ]

            movies_found[index+1] = {"movie_year": movie_year, "rating": rating, "voters": voters, "director": director,"actor_names":actor_names,"runtime":runtime,"genre":genre,"description":description}

movie_details(url)
movies_found = sorted(movies_found.items(), key = lambda x: x[1]["rating"])
movies_found = dict(movies_found)

movies_info = ["movie_year","rating","voters","director","actor_names","runtime","genre","description"]


with open('movies.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = movies_info)
    writer.writeheader()
    writer.writerows(movies_found)


# with open(f'movies_found.json', "w") as file:
#     json.dump(movies_found, file, indent=4)

print("Done")