from bs4 import BeautifulSoup
import requests


def get_last_page_num(url, last_page_css):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    return int(soup.select_one(last_page_css).text)


def get_goods_id(href):
    temp1, temp2, goods_id = href.rpartition('/')

    return goods_id


def get_img_src(src):
    temp1, temp2, img_src = src.rpartition('img/')

    return img_src


def get_price(price):
    if 'del' in str(price):
        price.find().decompose()

    return ''.join([x for x in price if x.isdigit()])


def get_data(page_url):
    page_data = []
    html = requests.get(page_url).text
    soup = BeautifulSoup(html, 'html.parser')

    # ['href'], ['title'], .find()['data-original']
    infos = soup.select("#searchList > li > div.li_inner > div.list_img > a")
    brands = soup.select("#searchList > li > div.li_inner > div.article_info > p.item_title > a")
    prices = soup.select("#searchList > li > div.li_inner > div.article_info > p.price")

    for i in range(len(infos)):
        page_info = {}

        goods_id = get_goods_id(infos[i]['href'])
        title = infos[i]['title']
        img_src = get_img_src(infos[i].find()['data-original'])
        brand = brands[i].text
        price = get_price(prices[i])

        page_info['goods_id'] = goods_id
        page_info['title'] = title
        page_info['img_src'] = img_src
        page_info['brand'] = brand
        page_info['price'] = price

        page_data.append(page_info)

    return page_data


def crawl_top():
    url = "https://search.musinsa.com/category/001?page=%d"
    css_selector = "#goods_list > div.boxed-list-wrapper > div.thumbType_box.box > span.pagingNumber > span.totalPagingNum"
    last_page_num = get_last_page_num(url % 1, css_selector)

    for page_num in range(1, last_page_num + 1):
        data = get_data(url % page_num)

        for info in data:
            print(info)


crawl_top()