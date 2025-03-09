import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def crawl_blog(url):
    # selenium 설정
    options = Options()
    options.add_argument("--headless") # 브라우저를 숨긴채로 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 블로그 url 로드
    driver.get(url) 

    # iframe 요소 로드 후, 해당 iframe으로 전환
    iframe = driver.find_element(By.ID, "mainFrame")
    driver.switch_to.frame(iframe)

    # iframe 안의 페이지 로드 될때까지 기다리기
    driver.implicitly_wait(10)

    # 포스팅 제목을 추출
    post_title = driver.find_element(By.CSS_SELECTOR, 'div.se-title-text span')
    title = post_title.text if post_title else "제목을 찾을 수 없습니다."

    # 본문 내용을 추출
    post_content = driver.find_element(By.CSS_SELECTOR, 'div.se-main-container')
    post_text = post_content.text if post_content else "본문을 찾을 수 없습니다."

    # 브라우저 종료
    driver.quit()

    return title, post_text