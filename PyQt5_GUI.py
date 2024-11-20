from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PIL import Image, ImageOps

import main
import sys
import os
import cv2

detect = False

class memberCheckGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("딥러닝 boys")
        self.setGeometry(200,200,600,200)

        # image_path를 None으로 초기화
        self.image_path = None

        # GUI 초기 버튼생성
        memberPhotoInsertButton=QPushButton('회원사진 등록',self)
        memberPhotoUpdateButton=QPushButton('회원사진 수정',self)
        memberPhotoDeleteButton=QPushButton('회원사진 삭제',self)
        startAppButton=QPushButton('탐지 시작',self)
        stopAppButton=QPushButton('탐지 종료',self)
        closeAppButton=QPushButton('프로그램 종료',self)
        self.label=QLabel('헬스장 회원확인 시스템',self)

        # GUI 초기 버튼 위치
        memberPhotoInsertButton.setGeometry(290,50,100,30)
        memberPhotoUpdateButton.setGeometry(390,50,100,30)
        memberPhotoDeleteButton.setGeometry(490,50,100,30)
        startAppButton.setGeometry(290,100,100,30)
        stopAppButton.setGeometry(390,100,100,30)
        closeAppButton.setGeometry(490,100,100,30)
        self.label.setGeometry(20, 70, 230, 50)
        self.label.setFont(QFont("Arial", 25, QFont.Black))

        # 버튼 클릭시
        memberPhotoInsertButton.clicked.connect(lambda: self.memberInsertGUI(1)) # 회원사진 등록 클릭시
        memberPhotoUpdateButton.clicked.connect(lambda: self.memberInsertGUI(2)) # 회원사진 수정 클릭시
        memberPhotoDeleteButton.clicked.connect(self.memberDeleteGUI) # 회원사진 수정 클릭시
        startAppButton.clicked.connect(main.main)
        #closeAppButton.clicked.connect()
        closeAppButton.clicked.connect(self.closeApp)

    def mainPageGUI(self):
        
        if hasattr(self, 'Insert_window') and self.Insert_window.isVisible():
            self.Insert_window.close()
        elif hasattr(self, 'Delete_window') and self.Delete_window.isVisible():   
            self.Delete_window.close()
        
        if "tempPhoto.jpg" in os.listdir("./tempPhoto"):
            os.remove(f"./tempPhoto/tempPhoto.jpg")
        self.main_window = memberCheckGUI()
        self.main_window.show()

      
            
    
    def memberInsertGUI(self,typeNum): # 회원 사진 등록 버튼 클릭 시 GUI
        self.close()
        self.Insert_window = QMainWindow()
        
        if typeNum == 1:
            self.Insert_window.setWindowTitle("회원 사진 등록")
        elif typeNum == 2:
            self.Insert_window.setWindowTitle("회원 사진 수정")
        self.Insert_window.setGeometry(250, 250, 500, 300)

        self.backPageButton = QPushButton('뒤로가기',self.Insert_window)
        self.backPageButton.setGeometry(10,10,100,30)
        self.backPageButton.clicked.connect(self.mainPageGUI)

        self.nameText = QTextEdit(self.Insert_window)
        self.nameLabel=QLabel('회원 이름',self.Insert_window)
        self.nameText.setGeometry(350,60,100,30)
        self.nameLabel.setGeometry(290, 60, 100, 30)

        self.numberText = QTextEdit(self.Insert_window)
        self.numberLabel=QLabel('번호 뒷4자리',self.Insert_window)
        self.numberText.setGeometry(350,100,100,30)
        self.numberLabel.setGeometry(270, 100, 100, 30)
        
        self.photoshooting = QPushButton('카메라 켜기',self.Insert_window)
        self.photoshooting.setGeometry(350,140,100,30)
        self.photoshooting.clicked.connect(self.cv2cam) # 카메라 실행

        self.photoInsert = QPushButton('사진 찾기',self.Insert_window)
        self.photoInsert.setGeometry(350,170,100,30)
        self.photoInsert.clicked.connect(self.memberPhotoSelect)

        self.imageLabel = QLabel(self.Insert_window)  # QLabel을 생성하여 이미지를 표시할 준비
        self.imageLabel.setGeometry(50, 60, 200, 200)

        self.insertButton = QPushButton('회원 등록',self.Insert_window)
        self.insertButton.setGeometry(350,200,100,30)
        self.insertButton.clicked.connect(lambda: self.memberPhotoInsert(self.image_path, self.nameText.toPlainText(), self.numberText.toPlainText()))
        
        self.Insert_window.show()

    def memberPhotoSelect(self):  # 사진 찾기 
        # QFileDialog 사용
        options = QFileDialog.Options()

        # '읽기 전용' 옵션을 제거하면 수정 가능
        self.image_path, _ = QFileDialog.getOpenFileName(
            self,  # 부모 위젯이 없으면 None을 사용
            "등록할 회원사진을 선택하세요",
            "",
            "Image Files (*.jpg *.jpeg *.png *.bmp)",
            options=options
        )
        self.imageLabelSet()

    def imageLabelSet(self):

        if self.image_path:
            # 이미지를 열고 크기를 조정
            img = Image.open(self.image_path)  # Pillow의 Image 모듈 사용
            img = ImageOps.exif_transpose(img) # 미지의 방향을 올바르게 조정
            
            # 가로를 200으로 고정하고 비율에 따라 세로 크기 계산
            #base_width = 200
            #w_percent = base_width / float(img.width)  # 가로 비율 계산
            #h_size = int((float(img.height) * w_percent))  # 세로 크기 계산
            #img_resized = img.resize((base_width, h_size)).convert("RGBA")  # 크기 조정 및 RGBA 변환

            # 가로를 200으로 고정하고 비율에 따라 세로 크기 계산
            base_width = 300
            base_height = 400
            img_resized = img.resize((base_width, base_height)).convert("RGBA")  # 크기 조정 및 RGBA 변환

            # QImage 생성
            data = img_resized.tobytes("raw", "RGBA")  # 크기 조정된 이미지를 바이트 데이터로 변환
            q_image = QImage(data, img_resized.width, img_resized.height, QImage.Format_RGBA8888)

            # QPixmap으로 변환
            pixmap = QPixmap.fromImage(q_image)
            self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio))

            print(f"선택된 이미지: {self.image_path}")
            
        else:
            print('이미지가 선택되지 않았습니다.')


    def memberPhotoInsert(self,img_path,name,number):  # 사진 등록 
        image_path = img_path
        userName = name
        userNumber = number

        if image_path and userName and userNumber:
            img = Image.open(image_path)  # Pillow의 Image 모듈 사용
            img = ImageOps.exif_transpose(img) # 미지의 방향을 올바르게 조정
            #img = ImageOps.mirror(img)  # 이미지 좌우 반전
                  
            # 가로를 300으로 고정하고 비율에 따라 세로 크기 계산
            base_width = 300
            w_percent = base_width / float(img.width)  # 가로 비율 계산
            h_size = int((float(img.height) * w_percent))  # 세로 크기 계산
            img = img.resize((base_width, h_size)) # 크기 조정 및 RGBA 변환

            
            # 저장할 폴더 경로
            save_folder = './memberPhoto'
            os.makedirs(save_folder, exist_ok=True)  # 폴더가 없으면 생성

            # 저장할 경로 및 파일명 지정
            save_path = os.path.join(save_folder, os.path.basename(userName+userNumber+'.jpg'))

            # 이미지 저장
            #img_resized.save(save_path)
            img.save(save_path)
            print(f'이미지가 {save_path}에 저장되었습니다.')
            if "tempPhoto.jpg" in os.listdir("./tempPhoto"):
                os.remove(f"./tempPhoto/tempPhoto.jpg")
            self.mainPageGUI()
        else:
            print('이미지, 이름 또는 번호가 입력되지 않았습니다.')

    def cv2cam(self):
        # 카메라 초기화
        cap = cv2.VideoCapture(0)  # '0'은 기본 카메라를 의미합니다.

        if not cap.isOpened():
            print("카메라를 열 수 없습니다!")
            exit()

        # 카메라 프레임 크기 설정 (300x300)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

        # 카메라 화면 열기
        print("스페이스바를 눌러 사진을 찍고, ESC를 눌러 종료하세요.")
        while True:
            ret, frame = cap.read()  # 프레임 읽기
            if not ret:
                print("프레임을 가져올 수 없습니다!")
                break

            cv2.imshow("Camera (300x300)", frame)  # 화면에 표시

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC 키
                print("종료합니다.")
                break
            elif key == 32:  # 스페이스바
                # 사진 저장
                filename = "./tempPhoto/tempPhoto.jpg"
                cv2.imwrite(filename, frame)
                print(f"사진이 저장되었습니다")

                self.image_path = filename
                break
                
        # 카메라 및 창 닫기
        cap.release()
        cv2.destroyAllWindows()
        self.imageLabelSet()



    def memberDeleteGUI(self): # 회원 사진 삭제 버튼 클릭 시 GUI
        self.close()
        self.Delete_window = QMainWindow()
        
        self.Delete_window.setWindowTitle("회원 삭제")
        self.Delete_window.setGeometry(250, 250, 250, 250)

        self.backPageButton = QPushButton('뒤로가기',self.Delete_window)
        self.backPageButton.setGeometry(10,10,100,30)
        self.backPageButton.clicked.connect(self.mainPageGUI)

        self.nameText = QTextEdit(self.Delete_window)
        self.nameLabel=QLabel('회원 이름',self.Delete_window)
        self.nameText.setGeometry(120,60,100,30)
        self.nameLabel.setGeometry(60, 60, 100, 30)

        self.numberText = QTextEdit(self.Delete_window)
        self.numberLabel=QLabel('번호 뒷4자리',self.Delete_window)
        self.numberText.setGeometry(120,100,100,30)
        self.numberLabel.setGeometry(40, 100, 100, 30)

        self.deleteButton = QPushButton('회원 삭제',self.Delete_window)
        self.deleteButton.setGeometry(70,170,100,30)
        self.deleteButton.clicked.connect(lambda: self.memberPhotoDelete(self.nameText.toPlainText(), self.numberText.toPlainText()))
        
        self.Delete_window.show()

    def memberPhotoDelete(self,name,number):   
        os.remove(f"./memberPhoto/{name}{number}.jpg")
        self.mainPageGUI()
    
    def closeApp(self):
        self.close()  # GUI 창을 닫고 애플리케이션 종료
        print('프로그램 종료!')

app=QApplication(sys.argv)
win =memberCheckGUI()
win.show()
app.exec_()

