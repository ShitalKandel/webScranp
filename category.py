import requests
from bs4 import BeautifulSoup
import webbrowser

url2 = "https://www.jobsnepal.com/category"

def job_category(url):
    resp = requests.get(url)
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

        return li  

def links(url):
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        a_links = soup.find_all('a', class_='jobs-category', limit=10)
        href_list = [link['href'] for link in a_links]
        
        job_categories = job_category(url)  
        
        print("\n<--Associating job categories with URLs-->")
        for i, (item, url) in enumerate(zip(job_categories, href_list), start=1):
            print(f"{i}: {item} - {url}")

        job_type_input = int(input("\nEnter the index according to the list: "))
        if 1 <= job_type_input <= len(job_categories):
            selected_category = job_categories[job_type_input - 1]
            selected_link = href_list[job_type_input - 1]
            print(f"\nSelected Job Category: {selected_category}")
            print(f"Opening link: {selected_link}")
            
            
            webbrowser.open(selected_link)
            title = soup.find_all('p',class_ = 'mb-0')
            location = soup.find_all('div', class_="d-flex align-items-center pl-1 pr-1 py-1").text
            

        else:
            print("Invalid index. Please enter a valid index.")

# Call the function to start the process
links(url2)
