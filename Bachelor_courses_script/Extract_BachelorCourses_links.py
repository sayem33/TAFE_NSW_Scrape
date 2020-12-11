"""Description:
    * author: Sayem Rahman
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 27-10-20
    * description:This script extracts all the courses links and save it in txt file.
"""
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pathlib import Path
from selenium import webdriver
from urllib.parse import urljoin
import bs4 as bs4
import requests
import lxml.html
import os
import re

def get_page(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return bs4.BeautifulSoup(r.content, 'html.parser')
    except Exception as e:
        pass
    return None

def clean_tags(soup_):
    for tag in soup_.find_all("tr", class_='hidethis'):
        tag.decompose()

# selenium web driver
# we need the Chrome driver to simulate JavaScript functionality
# thus, we set the executable path and driver options arguments
# ENSURE YOU CHANGE THE DIRECTORY AND EXE PATH IF NEEDED (UNLESS YOU'RE NOT USING WINDOWS!)
option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE

course_type_links = []
course_links = []
each_url = 'https://www.tafensw.edu.au/search?q=bachelor&disableFilters=qualification'
browser.get(each_url)
real_url = 'https://www.tafensw.edu.au/courses'
pure_url = each_url.strip()
each_url = browser.page_source

soup = bs4.BeautifulSoup(each_url, 'html.parser')
clean_tags(soup)

#each_courses_links = soup.find_all('h3' , class_='course-title')


each_courses_links = soup.find_all('a', href=re.compile('^/course/-/c/c'))
if each_courses_links:
    for a in each_courses_links:
        link = a['href']
        link = urljoin(real_url, link)
        course_links.append(link)
print(*course_links, sep='\n')

# each_courses_links = soup.find_all('h3', {'class': 'course-title'})
# if each_courses_links:
#     for a_tag in each_courses_links:
#         a = a_tag.find('a', href=True)
#         link = a['href']
#         link = urljoin(real_url, link)
#         course_links.append(link)
# print(*course_links, sep='\n')

course_links_file_path = os.getcwd().replace('\\', '/') + '/tafe_bachelor_links.txt'
course_links_file = open(course_links_file_path, 'w')

print(len(each_courses_links))

for i in course_links:
    if i is not None and i is not "" and i is not "\n":
        if i == course_links[-1]:
            course_links_file.write(i.strip())
        else:
            course_links_file.write(i.strip()+'\n')

course_links_file.close()

