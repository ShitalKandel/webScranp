import requests
import json
from bs4 import BeautifulSoup


# url = 'https://www.jobsnepal.com/'

# r = requests.get(url)

#r.text provides html 
# print(r.text)

#r.url provides the url link 
# print(r.url)

# print(r.status_code) #sends msg  whether get request can be fullfilled or not

# print(r.headers['content-type'])#provides unicode transformation format(UTF)

# print(r.content)#provides the content of the site in utf format

# print(r.json())#provides the data in dict format
# print(type(r.json()))

#provides directories that are used in the url
# print(dir(r))

##Post requset

data = {'title':'Search Job -Find Jobs Vacancy in Nepal | JobsNepal'}
headers = {'content-type':'application/json; charset = UTF-8'}

#data=json is used to convert python files into json format wher json.dumps make the file in 
# serialized format like {key : value }

# response = requests.post(url, data=json.dumps(data), headers=headers)

# print(response.status_code)#provides the server response message 

# print(response.ok)#boolean data types , provides if the response is true of false 

# print(type(response.text))#provides it's type 

# print(response.encoding)#provides its UTF port


# response = requests.post(url, data=json.dumps(data), headers=headers)
# print(response.status_code)

# r = requests.delete(url,data=json.dumps(data), headers = headers )
# print(r.status_code)





url = "view-source:https://www.jobsnepal.com/search?q=it+jobs"


response = requests.get(url)

print(response.status_code)
