#crawling entire one youtube playlist
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

#보관함(playlist)의 url, 공개로 전환해두기
#팝송가사
url = 'https://www.youtube.com/playlist?list=PLKZM3vsUUZm3HbcXnq6HlAe26RPkwBFU9'
#MA
# url = 'https://www.youtube.com/playlist?list=PLKZM3vsUUZm2PTEWff4oth-7wNV64qhSu'
#짬통
# url = 'https://www.youtube.com/playlist?list=PLKZM3vsUUZm1fnIO8i5Wk4HtELfLmcvo9'

def file_write(key_name_list:list):
    file = open('./test.txt', 'a', encoding='utf8')
    
    for key_name in key_name_list:
        file.write(key_name[0])
        file.write('\t')
        file.write(key_name[-1])
        file.write('\n')
        
    file.write('\n\n')
    file.write(str(len(key_name_list)))
    
    file.close()

def crawling_playlist(driver:webdriver.Chrome):
    soup = BeautifulSoup(driver.page_source,'html.parser')
    key_name_list=[]
    
    video_list = soup.select('#contents > ytd-playlist-video-renderer')
    for video in video_list:
        video_title = video.select_one('#video-title')
        
        href = video_title['href']
        key = href.split('&')[0].split('=')[-1]
        
        name = video_title.string.lstrip().rstrip()
        
        key_name_list.append((key,name))
    print(len(key_name_list))
    return key_name_list

def open_driver():
    global url
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    return driver
    
def scroll_down(driver:webdriver.Chrome):
    SCROLL_PAUSE_TIME = 1.5

    # Get scroll height
    # last_height = driver.execute_script("return document.querySelector('#contents > ytd-playlist-video-list-renderer').scrollHeight")
    last_height = driver.execute_script("return document.querySelector('#primary').scrollHeight")

    while True:
        # Scroll down to bottom
        # driver.execute_script("window.scrollTo(0, document.querySelector('#contents > ytd-playlist-video-list-renderer').scrollHeight);")
        driver.execute_script("window.scrollTo(0, document.querySelector('#primary').scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        # new_height = driver.execute_script("return document.querySelector('#contents > ytd-playlist-video-list-renderer').scrollHeight")
        new_height = driver.execute_script("return document.querySelector('#primary').scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    

def control_driver(driver:webdriver.Chrome):
    scroll_down(driver)
    

def main():
    driver = open_driver()
    control_driver(driver)
    key_name_list = crawling_playlist(driver)
    file_write(key_name_list)
    driver.close()

if __name__ == '__main__':
    main()