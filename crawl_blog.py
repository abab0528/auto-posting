from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup

# selenium으로 웹 페이지 열기
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 웹페이지 열기
# https://blog.naver.com/hi_nahyunii/223773706308
url = input("블로그의 url을 입력하세요: ")

driver.get(url)

# iframe 요소 로드 후, 해당 iframe으로 전환
iframe = driver.find_element(By.ID, "mainFrame")
driver.switch_to.frame(iframe)

# iframe 안의 페이지 로드 될때까지 기다리기
driver.implicitly_wait(10)

# 포스팅 제목을 추출
post_title = driver.find_element(By.CSS_SELECTOR, 'div.se-title-text span')
if post_title:
    print("포스팅 제목:", post_title.text)
else:
    print("포스팅 제목을 찾을 수 없습니다.")

# 본문 내용을 추출
post_content = driver.find_element(By.CSS_SELECTOR, 'div.se-main-container')
if post_content:
    print("포스팅 내용:", post_content.text)
else:
    print("본문 내용을 찾을 수 없습니다.")

# 브라우저 종료
driver.quit()