import requests
from bs4 import BeautifulSoup
res = requests.get("https://docs.python-requests.org/en/latest/user/install/")

soup = BeautifulSoup(res.text, "html.parser")
# print(soup.find("div"))
print(soup.find_all("a", recursive=False))
