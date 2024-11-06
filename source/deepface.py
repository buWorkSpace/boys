import cv2
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from deepface import DeepFace
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 나눔고딕 폰트를 기본 폰트로 설정
plt.rc('font', family='NanumGothic')
# 한글 폰트 설정 (예: 나눔고딕)
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # 시스템에 맞는 폰트 경로로 설정
fontprop = font_manager.FontProperties(fname=font_path)

# 입력 이미지 불러오기
img_path = '/content/drive/MyDrive/Colab Notebooks/deepface_img/test2.jpg'
img = cv2.imread(img_path)

# 얼굴 이미지 저장 경로
db_path = '/content/drive/MyDrive/Colab Notebooks/member_img'

try:
    # 얼굴 식별
    result = DeepFace.find(img_path=img_path,
                           db_path=db_path,
                           detector_backend='retinaface',
                           model_name='ArcFace')

    # 임계값 설정 (예: 0.4)
    threshold = 0.5
    df = result[0]

    # 첫 번째 매칭 결과의 distance 값 확인
    distance = df['distance'].iloc[0]
    print("distance" , distance)
    # 결과 True / False 판단
    is_match = distance <= threshold
    print("Match Found:", is_match)  # True 또는 False 출력

    # 결과 검출 여부 확인
    if result and not result[0].empty and distance < 0.5:  # 결과가 비어있지 않은지 확인


        # 결과 시각화
        fig = plt.figure()
        rows = 1
        cols = 2
        ax1 = fig.add_subplot(rows, cols, 1)
        ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax1.axis("off")

        # 가장 유사한 얼굴 이미지 가져오기 및 시각화
        res_img_path = df['identity'].iloc[0]
        res_img = cv2.imread(res_img_path)
        ax2 = fig.add_subplot(rows, cols, 2)
        ax2.imshow(cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB))
        ax2.axis("off")

        # 일치 여부를 제목으로 표시
        title_text = "등록된 회원입니다. " + str(is_match)
        plt.suptitle(title_text,fontproperties=fontprop)
        plt.show()

    else:
        # 매칭된 얼굴이 없는 경우 입력 이미지만 표시
        print("No matching faces found in the database.")

        # 검출 실패 시 입력 얼굴 이미지 표시
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.axis("off")
        plt.title("미등록 회원입니다.", fontproperties=fontprop)  # 한글 메시지 설정
        plt.show()

except Exception as e:
    print("An error occurred:", e)
