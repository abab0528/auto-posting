from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_post():
    new_topic = request.form['new_topic']
    audience = request.form['audience']
    length = request.form['length']
    keywords = request.form['keywords']
    format_choice = request.form['format_choice']

    image_file = request.files.get('image')
    if image_file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_path)
    else:
        image_path = None
        print("업로드된 이미지가 없습니다.")

    # 받은 입력값 출력
    print(f"주제: {new_topic}")
    print(f"독자층: {audience}")
    print(f"글 길이: {length}")
    print(f"포스팅 형식: {format_choice}")
    print(f"업로드된 이미지 경로: {image_path}")

    return "포스팅이 성공적으로 생성되었습니다!"

if __name__ == '__main__':
    app.run(debug=True)