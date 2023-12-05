import base64
import io
import requests
from PIL import Image
from bs4 import BeautifulSoup
import psycopg2

from urllib.request import Request, urlopen

def list_actors():
    conn = psycopg2.connect(dbname='IMDB_INFO', user='postgres', password='admin')
    cur = conn.cursor()
    cur.execute('SELECT * FROM "Actors"')
    rows = cur.fetchall()

    actor_names = []

    for row in rows:
        # Append the actor to the list
        actor_names.append(row[1])

    cur.close()
    conn.close()

    return actor_names


def show_name(id):
    conn = psycopg2.connect(dbname='IMDB_INFO', user='postgres', password='admin')
    cur = conn.cursor()
    query = 'SELECT * FROM "Actors" WHERE "ID" = ' + str(id)
    cur.execute(query)
    rows = cur.fetchone()
    cur.close()
    conn.close()
    name = rows[1]

    return name

def show_info(id):
    # TODO: Implement this method

    conn = psycopg2.connect(dbname='IMDB_INFO', user='postgres', password='admin')
    cur = conn.cursor()

    query = 'SELECT * FROM "Actors" WHERE "ID" =' + str(id)

    print(query)
    cur.execute(query)
    rows = cur.fetchone()
    cur.close()
    conn.close()
    description = rows[2]

    return description


def show_image(id):

    conn = psycopg2.connect(dbname='IMDB_INFO', user='postgres', password='admin')
    cur = conn.cursor()
    query = 'SELECT * FROM "Actors" WHERE "ID" = ' + str(id)
    cur.execute(query)
    rows = cur.fetchone()
    cur.close()
    conn.close()
    image_str = rows[3]

    return image_str


def scrape_full_description(description_url):

    site = description_url
    print(description_url)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    bio_div = soup.findAll('div', {'class': 'ipc-html-content ipc-html-content--base ipc-metadata-list-item-html-item'})
    if bio_div is not None:
        bio = bio_div[0].text.strip()
        return bio
    else:
        return "None"



def scrape_data():

    # Connect to your postgres DB
    conn = psycopg2.connect(dbname='IMDB_INFO', user='postgres', password='admin')
    cur = conn.cursor()

    # Create the table in your database

    # Get the webpage
    url = 'https://www.imdb.com/list/ls053501318/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    actors = soup.find_all('div', class_='lister-item mode-detail')

    if actors is not None:

        cur.execute('''TRUNCATE TABLE "Actors" RESTART IDENTITY;''')

        for actor in actors:

            # Get the actor name
            name = actor.find('h3').find('a').text.strip()
            # Get the actor description
            description_url = actor.find('h3').find('a', href = True)

            description_url = "https://www.imdb.com" + description_url['href'] + "/bio"
            print(description_url)

            description = scrape_full_description(description_url)


            #description = actor.find_all('p')[1].text.strip()
            # Get the actor image
            image_div = actor.find('div', class_='lister-item-image')


            if image_div is not None:
                image_tag = image_div.find('img')
                if image_tag is not None:
                    image_url = image_tag['src']
                    # Download the image
                    image_response = requests.get(image_url)
                    image = Image.open(io.BytesIO(image_response.content))
                    # Convert the image to binary format
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue())
                else:
                    img_str = None
            else:
                print("Warning: Can't find image of actor " + name)
                img_str = None

            cur.execute('''
                    INSERT INTO "Actors" (name, description, image) VALUES (%s, %s, %s)
                ''', (name, description, img_str))

            conn.commit()

    cur.close()
    conn.close()


class IMDB:

    def all_time_movies(self, name):
        # TODO: Implement this method

        pass

    def awards(self, name):
        # TODO: Implement this method
        pass

    def movie_genre(self, name):
        # TODO: Implement this method
        pass

    def average_rating(self, name):
        # TODO: Implement this method
        pass

    def top_movies(self, name):
        # TODO: Implement this method
        pass
