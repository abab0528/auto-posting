import requests
from flask import Flask, render_template, request, redirect, url_for, session
import os
from generate_post import generate_post_with_gpt
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'

load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")
redirect_uri = os.getenv("NAVER_REDIRECT_URI")

# 네이버 OAuth 2.0 인증 URL
oauth_url = os.getenv("OAUTH_URL")
token_url = os.getenv("TOKEN_URL")

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return '네이버 블로그 API 연동을 위한 OAuth 인증을 시작하세요'

@app.route('/login')
def login():
    auth_url = f"{oauth_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    print(auth_url)
    return redirect(auth_url)

@app.route('/naver/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'OAuth 인증 실패'
    
    parmas = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }

    response = requests.get(token_url, params=parmas)
    data = response.json()

    if 'access_token' in data:
        session['access_token'] = data['access_token']
        return '인증 성공'
    else:
        return 'Access Token을 얻지 못했습니다.'

@app.route('/generate')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_post():
    blog_url = request.form['blog_url']
    new_topic = request.form['new_topic']
    audience = request.form['audience']
    length = request.form['length']
    keywords = request.form['keywords']
    format_choice = request.form['format_choice']

    image_file = request.files.get('image')
    if image_file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)
        image_url = image_path
    else:
        image_url = None

    # 받은 입력값 출력
    print(f"블로그 주소: {blog_url}")
    print(f"주제: {new_topic}")
    print(f"독자층: {audience}")
    print(f"글 길이: {length}")
    print(f"포스팅 형식: {format_choice}")
    print(f"업로드된 이미지 경로: {image_url}")

    #자동 포스팅 생성
    generated_post = generate_post_with_gpt(blog_url, new_topic, audience, length, keywords, format_choice, image_url)

    if not generated_post:
        return "포스팅 생성에 실패하였습니다. 다시 시도해 주세요."
    

    return f"포스팅이 성공적으로 생성되었습니다: {generated_post[:100]}..."

if __name__ == '__main__':
    app.run(debug=True)