import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from PIL import Image
from dotenv import load_dotenv
import os
import glob
import shutil  # 디렉토리 삭제에 사용

def resize_image(input_path, output_path, max_width, max_height):
    try:
        with Image.open(input_path) as img:
            img.thumbnail((max_width, max_height))  # 이미지 크기 조정
            os.makedirs(os.path.dirname(output_path), exist_ok=True)  # 출력 디렉토리 생성
            img.save(output_path, format="JPEG")  # JPEG 형식으로 저장
    except Exception as e:
        print(f"이미지 리사이즈 중 오류 발생: {e}")
        raise


def emailSend(track_id):
    print("이메일 전송 시작")

    # .env 파일에서 환경 변수 로드
    load_dotenv()

    RECIPIENT_ID = os.environ.get("RECIPIENT_ID")
    NAVER_ID = os.environ.get('NAVER_ID')
    NAVER_PASS = os.environ.get('NAVER_PASS')
    
    recipients = [RECIPIENT_ID]

    message = MIMEMultipart()
    message['Subject'] = '등록되지 않은 회원 부정 출입 감지'
    message['From'] = NAVER_ID
    message['To'] = ",".join(recipients)

    # HTML 내용 작성
    content = """
        <html>
        <body>
            <h2>{title}</h2>
            <p>등록되지 않은 회원의 사진을 확인해주세요:</p>
    """.format(
        title='등록되지 않은 회원 부정 출입 감지'
    )

    # 특정 조건의 파일만 필터링
    image_folder = "./checkFaceFolder/"
    resized_folder = "./checkFaceFolder/resized/"
    all_files = glob.glob(os.path.join(image_folder, "*.jpg"))
    image_paths = [file for file in all_files if os.path.basename(file).startswith(f"face_id{track_id}")]
    

    if not image_paths:
        print("첨부할 이미지가 없습니다.")
        return

    resized_images = []

    # 각 이미지 크기 조정 및 HTML 내용 추가
    for idx, image_path in enumerate(image_paths):
        resized_image_path = os.path.join(resized_folder, f"face_resized_{idx}.jpg")
        try:
            resize_image(image_path, resized_image_path, max_width=200, max_height=200)
            resized_images.append(resized_image_path)
            content += f'<span><img src="cid:image_{idx}"></span>'
        except FileNotFoundError:
            print(f"이미지 파일을 찾을 수 없습니다: {image_path}")
            continue

    content += """
        </body>
        </html>
    """

    mimetext = MIMEText(content, 'html')
    message.attach(mimetext)

    # 리사이즈된 이미지 첨부
    for idx, resized_image_path in enumerate(resized_images):
        try:
            with open(resized_image_path, 'rb') as img:
                mimeimage = MIMEImage(img.read())
                mimeimage.add_header('Content-ID', f'<image_{idx}>')
                mimeimage.add_header('Content-Disposition', 'inline', filename=os.path.basename(resized_image_path))
                message.attach(mimeimage)
        except FileNotFoundError:
            print(f"이미지 파일을 찾을 수 없습니다: {resized_image_path}")
            continue


    # SMTP 서버 연결 및 이메일 전송
    try:
        server = smtplib.SMTP('smtp.naver.com', 587)
        server.ehlo()
        server.starttls()
        server.login(NAVER_ID, NAVER_PASS)
        server.sendmail(message['From'], recipients, message.as_string())
        server.quit()
        print("이메일 전송 성공")
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")

    # 리사이즈 폴더 삭제
    try:
        shutil.rmtree(resized_folder) 
    except Exception as e:
        print(f"리사이즈 폴더 삭제 중 오류 발생: {e}")


