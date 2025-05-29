import re
import requests
from requests.models import Response
from bs4 import BeautifulSoup
from arabic_reshaper import reshape
from bidi.algorithm import get_display

def clean_text(text: str) -> str:
    # فقط حروف فارسی، فاصله و پرانتزها رو نگه می‌داریم
    cleaned = re.sub(r'[^\sآ-ی()]+', '', text)
    # فاصله‌های اضافه رو یکی می‌کنیم
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def check_website() -> Response | str:
    response = requests.get("http://chap-sch.ir/guide-books")
    if response.status_code in [200, 201, 202]:
        return response
    return "not connect"

def extract_site(response: Response):
    content = BeautifulSoup(response.content, "html.parser")
    div_main = content.find("div", attrs={"class": "view-content"})
    all_tables = div_main.find_all("table")
    for every_table in all_tables:
        all_tr = every_table.find_all("tr")
        for every_tr in all_tr:
            all_tds = every_tr.find_all("td")
            for every_td in all_tds:
                raw_text = every_td.text
                cleaned = clean_text(raw_text)
                reshaped = reshape(cleaned)
                displayed = get_display(reshaped)
                print(displayed)

response = check_website()
if isinstance(response, Response):
    extract_site(response)
else:
    print(response)