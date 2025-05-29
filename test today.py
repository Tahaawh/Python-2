from bs4 import BeautifulSoup
from requests import Response
from arabic_reshaper import reshape
from bidi.algorithm import get_display

def extract_site(response: Response):
    content = BeautifulSoup(response.content, "html.parser")  # اصلاح "html-parser" به "html.parser"
    div_main = content.find("div", attrs={"class": "view-content"})
    all_tables = div_main.find_all("table")  # find_all خودش لیست میده؛ نیازی به *list نداری

    for every_table in all_tables:
        all_tr = every_table.find_all("tr")
        for every_tr in all_tr:
            all_tds = every_tr.find_all("td")
            for every_td in all_tds:
                print(get_display(reshape(every_td.text)))

# فرض می‌کنم check_website() تابعی هست که response میده
response = check_website()
extract_site(response)