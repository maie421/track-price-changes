from stringgetter import getPageString
from bs4 import BeautifulSoup

def getProducts(string):
    bsObj = BeautifulSoup(string, "html.parser")
    ul = bsObj.find("ul", {"id":"productList"})  #아이템 리스트부분 추출
    lis = ul.findAll("li", {"class":"baby-product renew-badge"}) #각 아이템 추출

    for item in lis:
        #url
        a = item.find("a", {"class": "baby-product-link"})
        url = a.get('href')
        print("url:", url)

        #name
        div_name = item.find("div", {"class":"name"})
        name = div_name.getText()
        print("name:", name)

        #image
        dt_image = item.find("dt", {"class":"image"})
        image = dt_image.find("img").get('src')
        print("image:", image)

        #price
        price = item.find("strong", {"class":"price-value"}).getText()
        print("price:", price)

    print(len(lis))
    return []

for i in range(1, 6):
    url = "https://www.coupang.com/np/categories/502483?channel=plp_C2&page=" + str(i)
    pageString = getPageString(url)
    print(getProducts(pageString))