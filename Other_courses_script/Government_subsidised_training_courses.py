"""Description:
    * author: Sayem Rahman
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 27-10-20
    * description:This script extracts all the courses links and save it in txt file.
"""
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pathlib import Path
import re
from urllib.parse import urljoin

import bs4 as bs4
import requests


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
each_url = 'https://www.tafensw.edu.au/study/types-courses/subsidised-courses'
browser.get(each_url)
real_url = 'https://www.tafensw.edu.au/courses'
pure_url = each_url.strip()
each_url = browser.page_source


# LINK EXTRACTOR
soup = bs4.BeautifulSoup(each_url, 'html.parser')
clean_tags(soup)
#each_courses_links = [tag['href'] for tag in soup.select('p a[href]')]
each_courses_links = [tag['href'] for tag in soup.select('p a[href ^="https://www.tafensw.edu.au/course/"]')]

print(*each_courses_links, sep='\n')



# SAVE LINKS TO FILE
course_links_file_path = os.getcwd().replace('\\', '/') + '/government_subsided_courses_links.txt'
course_links_file = open(course_links_file_path, 'w')

#print(len(each_courses_links))

for i in each_courses_links:
    if i is not None and i != "" and i != "\n":
        if i == each_courses_links[-1]:
            course_links_file.write(i.strip())
        else:
            course_links_file.write(i.strip()+'\n')
course_links_file.close()
