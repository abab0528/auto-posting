import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def crawl_blog(blog_url):
    # 최신 포스팅 5개만
    num_posts = 5

    # 최신 게시물 URL 가져오기
    post_urls = get_latest_posts(blog_url, num_posts)

    # 콘텐츠
    full_content = ""

    # 각 포스팅 URL 크롤링
    for url in post_urls:
        # selenium 설정
        options = Options()
        options.add_argument("--headless") # 브라우저를 숨긴채로 실행
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # 블로그 url 로드
        driver.get(url) 

        # iframe 안의 페이지 로드 될때까지 기다리기
        driver.implicitly_wait(10)

        # 포스팅 제목을 추출
        post_title = driver.find_element(By.CSS_SELECTOR, 'div.se-title-text span')
        title = post_title.text if post_title else "제목을 찾을 수 없습니다."

        # 본문 내용을 추출
        post_content = driver.find_element(By.CSS_SELECTOR, 'div.se-main-container').text
        full_content += post_content + "\n\n"

        # 브라우저 종료
    driver.quit()

    return full_content

def get_latest_posts(blog_url, num_posts):
    # selenium 설정
    options = Options()
    options.add_argument("--headless") # 브라우저를 숨긴채로 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 블로그 url 로드
    driver.get(blog_url) 

    # iframe 안의 페이지 로드 될때까지 기다리기
    driver.implicitly_wait(10)

    # response = requests.get(blog_url)

    # # 요청이 성공하면 (status = 200)
    # if response.status_code == 200:
    #     soup = BeautifulSoup(response.text, 'html.parser')
        
    #     # HTML 구조 확인을 위해 출력해보기
    #     print(soup.prettify())  # HTML 구조를 출력하여 정확한 위치 확인


    # iframe 요소 로드 후, 해당 iframe으로 전환
    iframe = driver.find_element(By.ID, "mainFrame")
    driver.switch_to.frame(iframe)

    time.sleep(3)

    # 최신 포스트 링크 추출
    post_links = []
    posts = driver.find_elements(By.CSS_SELECTOR, 'ul.thumblist li a.link')

    for post in posts[:num_posts]:
        link = post.get_attribute('href')
        if link:
            post_links.append(link)

    driver.quit()

    return post_links