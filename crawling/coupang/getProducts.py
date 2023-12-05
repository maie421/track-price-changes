from stringgetter import getPageString
from bs4 import BeautifulSoup
import re


def getProducts(string):
    results_list = []
    bsObj = BeautifulSoup(string, "html.parser")
    ul = bsObj.find("ul", {"id": "productList"})  # 아이템 리스트부분 추출
    lis = ul.findAll("li", {"class": "baby-product renew-badge"})  # 각 아이템 추출

    for item in lis:
        # url
        a = item.find("a", {"class": "baby-product-link"})
        url = a.get('href')

        # 정규 표현식을 사용하여 productId와 categoryId 추출
        product_id_match = re.search(r'/vp/products/(\d+)', url)
        category_id_match = re.search(r'categoryId=(\d+)', url)

        # name
        div_name = item.find("div", {"class": "name"})
        name = div_name.getText()

        # image
        dt_image = item.find("dt", {"class": "image"})
        image = dt_image.find("img").get('src')

        # price
        price = item.find("strong", {"class": "price-value"}).getText()

        # 결과를 리스트에 추가
        results_list.append({
            'product_id': product_id_match.group(1) if product_id_match else None,
            'category_id': category_id_match.group(1) if category_id_match else None,
            'name': name,
            'image': image,
            'price': price
        })
    print(len(lis))

    sql_statement = "INSERT INTO log.products (name, product_id, category_id, image, price) VALUES "

    for result in results_list:
        price = result['price'].replace(',', '')

        values = f"('{result['name'].strip()}', {result['product_id']}, {result['category_id']}, '{result['image']}', {price})"
        sql_statement += values + ", "

    sql_statement = sql_statement.rstrip(", ")
    print(sql_statement)
    return []


# for j in [502483, 502484, 502485, 502486, 502487]:
for j in [502483]:
    for i in range(1, 2):
        url = "https://www.coupang.com/np/categories/" + str(j) + "?listSize=100&channel=plp_C2&page=" + str(i)
        pageString = getPageString(url)
        getProducts(pageString)
