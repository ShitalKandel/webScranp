import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


url = "https://www.jobsnepal.com/category"


def job_category(url:str|None) -> list|None :

    """
    resp requests url which is in string format
    cate stores the list of job categories , if http request is 200 it parse the html in text format else returns 'None'
    categories parse the 'a' tag from Beautiful soup with 'class' as 'jobs-category' also it parse the first 8 'a' tags
    """

    resp = requests.get(url)
    cate = []

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")

        categories = soup.find_all('a', class_='jobs-category', limit=8)
        for i in categories:
            cate.append(i.get_text())
        job_string = str(cate)
        job_cate = job_string.strip("[]").replace("\\n", "").strip().replace("       ","").strip()


        '''li is a list which store the list of job category in string format, also strips the "'" quotes
        and extra commas between the words'''
        li = list([word.strip("'") for word in job_cate.split(",")])


        #it prints the list of job categories by the index and li return the list of job categories 
        print("\t<--Job by categories-->")
        for i, item in enumerate(li, start=1):
            print(f"{i}: {item}")

        return li
    return None




def job_category_links(url):

    '''it takes url as arguments, a http request is made
    associated 'a' tag link is used as per the list of job categories with limit 10
    (while making list for job categories there was job categories joined together so 
    while making list it was seperated making a list of 10 )
    job categories function is called to so to associate the links with it's job category
    '''


    r = requests.get(url, headers={
        'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'})
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

            join_job_category = urljoin(url, selected_link)

            job_details = fetch_job_details(join_job_category)
            return job_details
        
        else:
            print("Invalid index. Please enter a valid index.")




def get_tags(url):

    '''url is pass as argument
    a div container containing all the required details is scrap
    title tags, location tags and links as list are made to store title 
    ,location and links is used to join the 'href' link inside the container
     to get the job opening date and it's deadline
    it returns title, location, and links in the list 
    '''

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        div_location_tags = soup.find_all("div", class_="col-md-12 mb-3")

        title_tags = []
        location_tags = []
        links = []

        for div_tag in div_location_tags:

            title_tag = div_tag.find("h2", class_="job-title")

            if title_tag:
                title_text = title_tag.a.text.strip()
                title_tags.append(title_text)

            location_tag = div_tag.find_all("li", class_=False)

            for li_tag in location_tag:

                div_text = li_tag.find('div', class_='d-flex align-items-center pl-1 pr-1 py-1')

                if div_text:

                    location_tags.append(div_text.text.strip())

            link_tag = title_tag.find("a")

            link = link_tag["href"] if link_tag else None

            links.append(link)

        return title_tags, location_tags, links
    
    else:

        print(f"Error: Unable to fetch: {response.status_code}")
        return None, None, None



def get_job_details(url):
    '''
    it stores the data and formats the dates 
    it returns job_open_on date and deadline if date is not present it
    returns None
    '''
    job_resp = requests.get(url)

    if job_resp.status_code == 200:
        job_soup = BeautifulSoup(job_resp.text, "html.parser")
        job_dates_container = job_soup.find('div', class_='job-post-date-info mb-4')

        if job_dates_container:
            job_open_on_tag = job_dates_container.find("span", class_="job-posted-on")
            deadline_tag = job_dates_container.find("span", class_="apply-deadline")

            if job_open_on_tag and deadline_tag:
                job_open_on = job_open_on_tag.text.strip()[3:]
                deadline = deadline_tag.text.strip()[3:]
                return job_open_on, deadline
        else:
            return None, None




def fetch_job_details(url):

    '''
    get_job_details is called 
    we have make a list,set name as description and processed_urls
    where description stores the title , location and dates of jobs 
    and processed urls stores links, from each job
    to fetch dates'''
    description = []
    processed_urls = set()

    tags = get_tags(url)

    if not tags:
        print("No tags found")

    title_tags, location_tags, links = tags

    for title_tag, location_tag, link in zip(title_tags, location_tags, links):
        title = title_tag.strip()
        if isinstance(location_tag, str):
            location = location_tag.strip() if location_tag else "N/A"
        else:
             location = location_tag.text.strip() if location_tag else "N/A"
        job_detail_url = link


        #condition is given if job links start with https if fetch job dates else is checks if the link
        #is in procesed urls else it skips 
        if job_detail_url.startswith("http") and job_detail_url not in processed_urls:
            job_open, deadline_job = get_job_details(job_detail_url)

            if job_open and deadline_job:
                job_open = " ".join(job_open.split()[2:])
                deadline_job = " ".join(deadline_job.split()[2:])
            else:
                print(f"Skipping job_detail_url without details: {job_detail_url}")

        elif not job_detail_url.startswith("http"):
            print(f"Skipping invalid job_detail_url: {job_detail_url}")

        values = {
            "title": title,
            "location": location,
            "apply-on":job_open,
            "deadline_job":deadline_job
        }


        description.append(values)

        processed_urls.add(job_detail_url)
            

    #it returns the dictinorary which contains all the values from each job category
    return description





# data = fetch_job_details(url)

'''
we made a variable to call the job_category_links , so while 
calling a variable url as an arguments is passed'''
data = job_category_links(url)


# name a csv file name 
csv_file_path = "dec_19.csv"


'''
Opened csv file name and assigned a header to store data as per their rows
data saved to file msg is sent after the scraping of the data is 
made successfully'''

with open(csv_file_path, "a", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["title", "location","apply-on","deadline_job"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if csv_file.tell() == 0:
        writer.writeheader()

    for row in data:
        writer.writerow(row)

print(f"Data has been saved to {csv_file_path}")
