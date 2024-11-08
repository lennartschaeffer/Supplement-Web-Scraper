from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def scrape_preworkout():
    pageSK = 1
    pagePS = 1
    isNextPageSK = True
    isNextPagePS = True
    products = []

    while isNextPageSK:
        url = "https://www.supplementking.ca/shop/products/pre-workout-products?p=" + str(pageSK)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.find_all("a", {"class": "product-item-link"})
        prices = soup.find_all("span", {"class": "price-wrapper"})
        urls = soup.find_all("a", {"class": "product-item-link"})
        images = soup.find_all("img", {"class": "product-image-photo"})

        AddProducts(images, prices, products, titles, urls, 'Supplement King', None)

        next_link = soup.find("a", {"title": "Next"})
        if next_link:
            next_url = next_link.get("href")
            if not next_url:
                isNextPageSK = False
            else:
                pageSK += 1
        else:
            isNextPageSK = False

    if isNextPageSK is False:
        while isNextPagePS:
            url = "https://shoppopeyes.com/en/collections/pre-entrainement-pre-workout?page=" + str(pagePS) + (
                "&grid_list"
                "=grid-view")
            print(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            titles = soup.find_all("h2", {"class": "productitem--title"})
            prices = soup.find_all("div", {"class": "price--main"})
            compare_prices = soup.find_all("div", {"class": "price--compare-at visible"})
            urls = soup.find_all("a", {"class": "productitem--image-link"})
            figures = soup.find_all('figure', class_='productitem--image')
            images = [figure.find('img') for figure in figures]

            AddProducts(images, prices, products, titles, urls, "Popeye's Supplements", compare_prices)

            next_link = soup.find("a", {"aria-label": "Go to next page"})

            if next_link:
                next_url = next_link.get("href")

                if not next_url:
                    isNextPagePS = False
                else:
                    pagePS += 1
            else:
                isNextPagePS = False

    return products


def scrape_protein():
    products = []

    urlSK = "https://www.supplementking.ca/shop/products/protein-powders"
    response = requests.get(urlSK)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all("a", {"class": "product-item-link"})
    prices = soup.find_all("span", {"class": "price-wrapper"})
    urls = soup.find_all("a", {"class": "product-item-link"})
    images = soup.find_all("img", {"class": "product-image-photo"})

    AddProducts(images, prices, products, titles, urls, 'Supplement King', None)

    urlPS = "https://shoppopeyes.com/en/collections/isolat-de-proteine-de-petit-lait-whey-protein-isolate"
    response = requests.get(urlPS)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all("h2", {"class": "productitem--title"})
    prices = soup.find_all("div", {"class": "price--main"})
    compare_prices = soup.find_all("div", {"class": "price--compare-at visible"})
    urls = soup.find_all("a", {"class": "productitem--image-link"})
    figures = soup.find_all('figure', class_='productitem--image')
    images = [figure.find('img') for figure in figures]

    AddProducts(images, prices, products, titles, urls, "Popeye's Supplements",compare_prices)

    return products

def scrape_creatine():
    products = []

    urlSK = "https://www.supplementking.ca/shop/products/creatine"
    response = requests.get(urlSK)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all("a", {"class": "product-item-link"})
    prices = soup.find_all("span", {"class": "price-wrapper"})
    urls = soup.find_all("a", {"class": "product-item-link"})
    images = soup.find_all("img", {"class": "product-image-photo"})

    AddProducts(images, prices, products, titles, urls, 'Supplement King', None)

    urlPS = "https://shoppopeyes.com/en/collections/creatine-creatine"
    response = requests.get(urlPS)
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.find_all("h2", {"class": "productitem--title"})
    prices = soup.find_all("div", {"class": "price--main"})
    compare_prices = soup.find_all("div", {"class": "price--compare-at visible"})
    urls = soup.find_all("a", {"class": "productitem--image-link"})
    figures = soup.find_all('figure', class_='productitem--image')
    images = [figure.find('img') for figure in figures]

    AddProducts(images, prices, products, titles, urls, "Popeye's Supplements",  compare_prices)

    return products

def AddProducts(images, prices, products, titles, urls, store, compare_prices):

    for i, (title, price, url, img) in enumerate(zip(titles, prices, urls, images)):
        if store == "Popeye's Supplements":
            url = 'https://shoppopeyes.com/' + url.get("href")
        else:
            url = url.get("href")

        price = str(price.get_text(strip=True))
        product = {
            'title': title.get_text(strip=True),
            'price': price[price.index('$'):len(price)],
            'url': url,
            'img': img.get("src"),
            'store': store
        }
        if compare_prices is not None and i < len(compare_prices):
            com_price = compare_prices[i].get_text(strip=True)
            index = com_price.find('$')
            product['compare_price'] = com_price[:index] + ' ' + com_price[index:]

        products.append(product)


@app.route("/")
def home():
    preworkouts = scrape_preworkout()
    proteins = scrape_protein()
    creatines = scrape_creatine()
    return render_template("index.html", preworkouts=preworkouts, proteins=proteins, creatines=creatines)


if __name__ == "__main__":
    app.run(debug=True)
