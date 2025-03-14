import openai
from openai import Client
import os
from dotenv import load_dotenv
from crawl_blog import crawl_blog
from generate_prompt import generate_prompt

# .env 파일에서 환경 변수 로드
load_dotenv()

# 환경 변수에서 OpenAI API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY2")

client = openai.Client(api_key = api_key)

# 블로그 스타일 예제
url = input("블로그의 url을 입력하세요: ")
sample_blog_post = crawl_blog(url)

# 블로그 글 스타일 분석을 위한 함수
def analyze_blog_style(blog_post):
    response = client.chat.completions.create(model="gpt-3.5-turbo",  # 사용하려는 모델
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"이 블로그 글의 스타일을 분석하고 톤, 구조, 언어를 설명해 주세요:\n\n{blog_post}"}
    ])
    return response.choices[0].message.content.strip()

# 블로그 글 스타일에 맞춘 새로운 블로그 글 생성 함수
def generate_blog_post_with_style(style_analysis, new_topic, audience, length, keywords, format_choice):
    combined_prompt = generate_prompt(style_analysis, new_topic, audience, length, keywords, format_choice)

    response = client.chat.completions.create(model="gpt-3.5-turbo",  # 사용하려는 모델
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": combined_prompt}
    ])
    return response.choices[0].message.content.strip()

# 예시 블로그 글 스타일 분석
if sample_blog_post:
    style_analysis = analyze_blog_style(sample_blog_post)
    print("Style Analysis:")
    print(style_analysis)

# 스타일에 맞춰 새로운 블로그 글 생성
new_topic = input("새로운 주제를 입력하세요: ")
audience = input("독자층을 입력하세요: ")
length = input("글 길이를 입력하세요(short/medium/long): ")
keywords = input("포함할 키워드를 입력하세요: ") 
format_choice = input("포스팅 형식을 입력하세요(list/blog/essay): ")
generated_blog = generate_blog_post_with_style(style_analysis, new_topic, audience, length, keywords, format_choice)
print("\nGenerated Blog Post:")
print(generated_blog)
