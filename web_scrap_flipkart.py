from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

#my_url="https://www.flipkart.com/search?q=samsung+mobiles&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_HistoryAutoSuggest_0_2&otracker1=AS_QueryStore_HistoryAutoSuggest_0_2&as-pos=0&as-type=HISTORY&as-searchtext=sa"

my_url = "https://www.flipkart.com/search?q=vivi%20mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")
containers = page_soup.findAll("div", { "class": "bhgxx2 col-12-12"})

# print('len: ',len(containers))
# container = containers[2]
# print(soup.prettify(containers[2]))

# # Name of items
# print(container.div.img["alt"])
# price = container.findAll("div", {"class": "_1vC4OE _2rQ-NK"})
# # print(price[0].text)
#
# ratings = container.findAll("div", {"class": "hGSR34"})
# # print(ratings[0].text)

filename = "products.csv"
f = open(filename, "w")

headers = "Product_Name, Pricing, Ratings, f1, f2, f3, f4, f5, f6,f7,f8 \n"
f.write(headers)

for container in containers:
    if not container.findAll("img", {"class": "_1Nyybr"}):
        continue
    # product_name = container.findAll("img", {"class": "_1Nyybr"})
    product_name = container.div.img["alt"]

    price_container = container.findAll("div", {"class": "_1vC4OE _2rQ-NK"})
    if not price_container[0].text:
        continue
    else:
        price = price_container[0].text

    rating_container = container.findAll("div", {"class": "hGSR34"})
    if not rating_container[0].text:
        continue
    else:
        rating = rating_container[0].text
    
    ulli = container.findAll("li", { "class": "tVe95H"})
    li_array = [];
    for li in ulli:
        li_array.append(li.text)

    # print("Product_Name:"+ product_name)
    # print("Price: " + price)
    # print("Ratings:" + rating)

    #String parsing
    trim_price=''.join(price.split(','))
    rm_rupee = trim_price.split('₹')
    add_rs_price = "Rs."+rm_rupee[1]
    split_price = add_rs_price.split('E')
    final_price = split_price[0]

    split_rating = rating.split(" ")
    final_rating = split_rating[0]

    # final_price = price
    # final_rating = rating
    str = ""
    for li in li_array:
        str += "," + li
    print(product_name.replace("," ,"|") +", " + final_price +",  " + final_rating + ",  " + str + "\n")

    str = ""
    for li in li_array:
        str += "," + li
    f.write(product_name.replace("," ,"|") +"," + final_price +"," + final_rating + str + "\n")

f.close()
