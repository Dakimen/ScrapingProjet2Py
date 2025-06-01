import requests
from bs4 import BeautifulSoup
import csv
import os
import re
from datetime import datetime

def getCategoryPages(url):
    response = requests.get(url)
    html = response.content
    landing_soup = BeautifulSoup(html, "html.parser")
    category_div = landing_soup.find_all("div", class_="side_categories")
    categories_ul = category_div[0].find_all("ul", class_="nav-list")
    categories_inner_ul = categories_ul[0].find_all("ul")
    categories_listed = categories_inner_ul[0].select("li")
    category_pages = []
    for category_listed in categories_listed:
        category_page = category_listed.find("a")["href"]
        category_pages.append(f"{url}{category_page}")
    return category_pages

def getBookPages(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    products = []
    next_page_area = soup.find_all("ul", class_="pager")
    if next_page_area:
        next_page_link_li = next_page_area[0].find_all("li", class_="next")
        while next_page_link_li:
            products_html = soup.select("article.product_pod")
            for product_html in products_html:
                title_h3 = product_html.find("h3")
                title_html = title_h3.find_all("a")
                href = title_html[0]["href"]
                products.append(href)
            next_page_link = next_page_link_li[0].find_all("a")
            next_page_url_ending = next_page_link[0]["href"]
            url_base = url.split("index.html")
            next_page_url = f"{url_base[0]}{next_page_url_ending}"
            next_response = requests.get(next_page_url)
            next_html = next_response.content
            soup = BeautifulSoup(next_html, "html.parser")
            next_page_area = soup.find_all("ul", class_="pager")
            next_page_link_li = next_page_area[0].find_all("li", class_="next")
    products_html = soup.select("article.product_pod")
    for product_html in products_html:
        title_h3 = product_html.find("h3")
        title_html = title_h3.find_all("a")
        href = title_html[0]["href"]
        products.append(href)
    return products

def downloadImage(imageurl, book_title, folder_name):
    now = datetime.now()
    current_time = now.strftime("%d%m%Y%H%M%S")
    delimiters = r"[,\;:|/()?!'\".&* ]"
    title_split = re.split(delimiters, book_title)
    spaceless_title = ""
    for segment in title_split:
        spaceless_title = f"{spaceless_title}{segment}"
    new_image_name = f"{spaceless_title}{current_time}.jpg"
    image_path = os.path.join(folder_name, new_image_name)
    response = requests.get(imageurl)
    if response.status_code == 200:
        with open(image_path, "wb") as file:
            file.write(response.content)
            print(f"Image saved successfully in: {image_path}")
    else:
        print("Failed to download image")
    

def getBooks(products, url_main, folder_name):
    books = []
    for product in products:
        product_split_url = product.split("../../../")
        product_fulladdress = f"{url_main}catalogue/{product_split_url[1]}"
        print(product_fulladdress)
        response_book = requests.get(product_fulladdress)
        book_page_soup = BeautifulSoup(response_book.content, "html.parser")
        book_title = book_page_soup.find("h1").get_text()
        td = book_page_soup.select("td")
        book_upc = td[0].get_text()
        price_incl = td[3].get_text()
        price_incl_number = price_incl.split("£")[1]
        price_excl = td[2].get_text()
        price_excl_number = price_excl.split("£")[1]
        available_raw_text = td[5].get_text()
        nb_available = available_raw_text.split("(")[1].split(" ")[0]
        description_div = book_page_soup.find(id="product_description")
        if description_div:
            description_text = description_div.find_next("p").get_text()
        else:
            description_text = ""
        breadcrumb = book_page_soup.find("ul")
        category = breadcrumb.select("a")[2].get_text()
        review_rating_nb = book_page_soup.select_one("p.star-rating")["class"][1]
        match review_rating_nb:
            case "One":
                review_rating_nb = 1
            case "Two":
                review_rating_nb = 2
            case "Three":
                review_rating_nb = 3
            case "Four":
                review_rating_nb = 4
            case "Five":
                review_rating_nb = 5
            case _:
                review_rating_nb = "error"
        review_rating = f"{review_rating_nb}/5"
        image_url = book_page_soup.find("img")["src"].split("media")[1]
        image_url = f"{url_main}media{image_url}"
        downloadImage(image_url, book_title, folder_name)
        book = []
        book.append(product_fulladdress)
        book.append(book_upc)
        book.append(book_title)
        book.append(price_incl_number)
        book.append(price_excl_number)
        book.append(nb_available)
        book.append(description_text)
        book.append(category)
        book.append(review_rating)
        book.append(image_url)
        books.append(book)
    return(books)

def write_csv(books):
    with open("books.csv", "w", encoding="utf-8", newline="") as file_csv:
        writer = csv.writer(file_csv, delimiter=",")
        en_tete = ["product_page_url","universal_product_code","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"]
        writer.writerow(en_tete)
        for book in books:
            for one_book in book:
                writer.writerow(one_book)