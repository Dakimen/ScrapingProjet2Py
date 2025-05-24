import scraper_functions

def main():
    url_main = "https://books.toscrape.com/"
    folder_name = "images"
    scraper_functions.os.makedirs(folder_name, exist_ok=True)
    print("Images folder created")
    category_pages = scraper_functions.getCategoryPages(url_main)
    print("Category pages recuperated")
    all_site_pages = []
    for category_page in category_pages:
        lists_books_per_page = scraper_functions.getBookPages(category_page, url_main)
        all_site_pages.append(lists_books_per_page)
    books = []
    print("All pages recuperated")
    for site_page in all_site_pages:
        new_books = scraper_functions.getBooks(site_page, url_main, folder_name)
        books.append(new_books)
    scraper_functions.write_csv(books)

main()