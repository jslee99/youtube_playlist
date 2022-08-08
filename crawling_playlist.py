#crawling entire one youtube playlist
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

#보관함(playlist)의 url
url = 'https://www.youtube.com/playlist?list=PLKZM3vsUUZm3S5gPeCc-tbPDdTW6EVArd'
#보관함 (playlist)비공개일시 control_driver함수 내부에서 login함수 호출 공개일시 login함수 호출 안해도 됨. 이때 login함수에서 쓰이게 될 email,pwd정보
email = ''
pwd = ''


def crawling_playlist(driver:uc.Chrome):
    soup = BeautifulSoup(driver.page_source,'html.parser')
    file = open('test.txt', 'a', encoding='utf8')
    
    video_list = soup.select('#contents > ytd-playlist-video-renderer')
    for video in video_list:
        file.write(video.select_one('#video-title').string.lstrip().rstrip())
        file.write('\n')
    file.write(str(len(video_list)))
    for i in range(0, 10):
        file.write('\n')
    file.close()
    print(len(video_list))

def open_driver():
    global url
    
    driver = uc.Chrome()
    driver.get(url)
    return driver

def login(driver:uc.Chrome):
    global email
    global pwd
    
    driver.find_element(By.CSS_SELECTOR,'#buttons > ytd-button-renderer').click()
#    driver.find_element(By.CSS_SELECTOR,'#view_container > div > div > div.pwWryf.bxPAYd > div > div.WEQkZc > div > form > span > section > div > div > div > div > ul > li:nth-child(2) > div > div > div.BHzsHc').click()
    driver.find_element(By.CSS_SELECTOR,'#identifierId').send_keys(email)
    driver.find_element(By.CSS_SELECTOR,'#identifierNext > div > button').click()
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input')))
    except:
        exit(0)
    
    driver.find_element(By.CSS_SELECTOR, '#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input').send_keys(pwd)
    driver.find_element(By.CSS_SELECTOR,'#passwordNext > div > button').click()
    
    #활동확인 기다리기
    try:
        WebDriverWait(driver, 400).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#contents')))
    except:
        exit(0)
    
    
def scroll_down(driver:uc.Chrome):
    SCROLL_PAUSE_TIME = 1.5

    # Get scroll height
    last_height = driver.execute_script("return document.querySelector('#contents > ytd-playlist-video-list-renderer').scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.querySelector('#contents > ytd-playlist-video-list-renderer').scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.querySelector('#contents > ytd-playlist-video-list-renderer').scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    

def control_driver(driver:uc.Chrome):
#플레이리스트가 공개일 경우에는 로그인 생략가능
    login(driver)
    scroll_down(driver)
    

def main():
    driver = open_driver()
    control_driver(driver)
    crawling_playlist(driver)
    driver.close()

if __name__ == '__main__':
    main()