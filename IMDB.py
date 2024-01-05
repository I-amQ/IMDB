import base64
import io

from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

import requests
from PIL import Image
from bs4 import BeautifulSoup
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

WINDOW_SIZE = "1920,1080"
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
web_driver = webdriver.Chrome(options=chrome_options)



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

def get_movies(id):

    conn = psycopg2.connect(dbname='IMDB_INFO', user='postgres', password='admin')
    cur = conn.cursor()
    query = 'SELECT movies FROM "Actors" WHERE "ID" = ' + str(id)
    cur.execute(query)
    rows = cur.fetchone()
    cur.close()
    conn.close()

    return rows[0]

def scrape_full_description(description_url):

    site = description_url
    #print(description_url)
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


def scrape_all_time_movies(description_url):

    global web_driver
    site = description_url
    #print(description_url)
    #hdr = {'User-Agent': 'Mozilla/5.0'}
    #req = Request(site, headers=hdr)
    #page = urlopen(req)
    #soup = BeautifulSoup(page, 'html.parser')

    web_driver.delete_all_cookies()
    web_driver.get(site)
    #wait = WebDriverWait(web_driver, 10)

    #try:
    WebDriverWait(web_driver, 100).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/button[1]'))).click()
    #decline_cookie_btn = web_driver.find_element(By.XPATH, '')
    #decline_cookie_btn.click()
    #except NoSuchElementException:
    #    pass
    #web_driver.execute_script("arguments[0].scrollIntoView();", EC.visibility_of_element_located((By.XPATH, '//*[@id="accordion-item-actor-previous-projects"]/div/div/span/button')))
    web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

    try:
        (WebDriverWait(web_driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                              '/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/div[4]/section[2]/div[5]/div[2]/div/div[4]/div/div/span/button')))
                                                        .click())
    except Exception:
        try:
            button = web_driver.find_element(By.XPATH,
                                             '//*[@id="accordion-item-actor-previous-projects"]/div/div/span/button')
            web_driver.execute_script("arguments[0].click();", button)
        except Exception:
            try:
                button = web_driver.find_element(By.XPATH,
                                                 '/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/div[4]/section[2]/div[5]/div[2]/div/div[4]/div/div/span/button')
                web_driver.execute_script("arguments[0].click();", button)
            except Exception:
                button = web_driver.find_element(By.CLASS_NAME, 'ipc-see-more__button')
                web_driver.execute_script("arguments[0].click();", button)
    #button = web_driver.find_element(By.XPATH, '//*[@id="accordion-item-actor-previous-projects"]/div/div/span/button')

    #web_driver.execute_script("arguments[0].scrollIntoView();", button)
    #web_driver.execute_script("arguments[0].click();", button)

    #button.click()

    soup = BeautifulSoup(web_driver.page_source, 'html.parser')
    actor_movies_section = soup.find('div', {'class': 'sc-6703147-3 jZGlkr'})
    movies_tags = actor_movies_section.find_all('a',{'class': 'ipc-metadata-list-summary-item__t'})

    movies = [movie.text.strip() for movie in movies_tags]

    return movies


def scrape_average_rating(description_url):
        # TODO: Implement this method



        pass

def scrape_data():
    global web_driver
    # Connect to your postgres DB
    conn = psycopg2.connect(dbname='IMDB_INFO', user='postgres', password='admin')
    cur = conn.cursor()

    # Create the table in your database

    # Get the webpage
    url = 'https://www.imdb.com/list/ls053501318/'
    #response = requests.get(url)
    web_driver.get(url)
    soup = BeautifulSoup(web_driver.page_source, 'html.parser')

    actors = soup.find_all('div', class_='lister-item mode-detail')

    if actors is not None:
        cur.execute('''
            TRUNCATE TABLE "Actors" RESTART IDENTITY;
        ''')

        for actor in actors:

            # Get the actor name
            name = actor.find('h3').find('a').text.strip()
            # Get the actor description
            bio_link = actor.find('h3').find('a', href = True)
            description_url = "https://www.imdb.com" + bio_link['href'].split("?")[0] + "/bio"
            print(description_url)
            description = scrape_full_description(description_url)
            movies_link = "https://www.imdb.com" + bio_link['href'].split("?")[0] + "/"
            print(movies_link)
            movies = scrape_all_time_movies(movies_link)

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
                    INSERT INTO "Actors" (name, description, image, movies) VALUES (%s, %s, %s, %s)
                ''', (name, description, img_str,(movies,)))

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



    def top_movies(self, name):
        # TODO: Implement this method




        pass