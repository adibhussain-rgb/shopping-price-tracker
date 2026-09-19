import requests
from bs4 import BeautifulSoup

url = "https://www.flipkart.com/shivaay-nano-glass-dji-mini-3-pro/p/itm61fda56028d62?pid=ACCHM9MR4QQZP4FG&lid=LSTACCHM9MR4QQZP4FGWSVWTI&marketplace=FLIPKART&store=4rr%2Fkm5%2Fipq%2Flrv&srno=b_1_1&otracker=browse&fm=organic&iid=8c875fd4-1802-4910-8a20-34543cfffa3f.ACCHM9MR4QQZP4FG.SEARCH&ppt=None&ppn=None&ssid=wyfqgrfppc0000001789825971203&ov_redirect=true&ov_redirect=true"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

price_tag = soup.find("div", class_="v1zwn21n v1zwn20 _1psv1zeb9 _1psv1ze0")
price_text = price_tag.text.replace("₹", "").replace(",", "")
price = float(price_text)
print(price)