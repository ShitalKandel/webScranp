import requests
from bs4 import BeautifulSoup

url2 = "https://www.jobsnepal.com/category"

def job_category(url2):
    resp = requests.get(url2)
    cate = []

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")

        categories = soup.find_all('a', class_='jobs-category', limit=8)
        for i in categories:
            cate.append(i.get_text())

        job_string = str(cate)
        job_cate = job_string.strip("[]").replace("\\n", "").strip().replace("       ","").strip()

        li = list([word.strip("'") for word in job_cate.split(",")])
        
        print("\t<--Job by categories-->")
        for i, item in enumerate(li, start=1):
            print(f"{i}: {item}")

def links(url2):
    r = requests.get(url2)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        a_links = soup.find_all('a', class_='jobs-category', limit=8)
        href_list = [link['href'] for link in a_links]
        return href_list

print(links(url2))
