import requests
from bs4 import BeautifulSoup
import csv

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

def getBookPages(url, url_main):
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
                title_html = title_h3.findChildren("a")
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
        title_html = title_h3.findChildren("a")
        href = title_html[0]["href"]
        products.append(href)
    return products
    

def getBooks(products, url):
    books = []
    for product in products:
        product_fulladdress = f"{url}{product}"
        response_book = requests.get(product_fulladdress)
        book_page_soup = BeautifulSoup(response_book.content, "html.parser")
        book_title = book_page_soup.find("h1").get_text()
        td = book_page_soup.select("td")
        book_upc = td[0].get_text()
        price_incl = td[3].get_text()
        price_excl = td[2].get_text()
        available_raw_text = td[5].get_text()
        nb_available = available_raw_text.split("(")[1].split(" ")[0]
        description_h2 = book_page_soup.find("h2")
        description_text = description_h2.find_next().get_text()
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
        image_url = f"{url}media{image_url}"
        book = []
        book.append(product_fulladdress)
        book.append(book_upc)
        book.append(book_title)
        book.append(price_incl)
        book.append(price_excl)
        book.append(nb_available)
        book.append(description_text)
        book.append(category)
        book.append(review_rating)
        book.append(image_url)
        books.append(book)
    return(books)

def write_csv(books):
    with open("books.csv", "w") as file_csv:
        writer = csv.writer(file_csv, delimiter=",")
        en_tete = ["product_page_url","universal_product_code","title","price_including_tax","price_excluding_tax","number_available","product_description","category","review_rating","image_url"]
        writer.writerow(en_tete)
        for book in books:
            writer.writerow(book)

def main():
    url_main = "https://books.toscrape.com/"
    category_pages = getCategoryPages(url_main)
    all_book_pages = []
    for category_page in category_pages:
        lists_books_per_page = getBookPages(category_page, url_main)
        for list_books_per_page in lists_books_per_page:
            all_book_pages.append(list_books_per_page)
    print(len(all_book_pages))

    #url = "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html"
    #print(len(products))
    #books = getBooks(products, url)
    #write_csv(books)

main()