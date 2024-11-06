import cv2
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from deepface import DeepFace
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np
import os
import tempfile

class FaceRecognition:
    def __init__(self, db_path='./memberPhoto', threshold=0.5):
        self.db_path = os.path.abspath(db_path)
        self.threshold = threshold
        
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database path not found: {self.db_path}")

    def compare_face_from_frame(self, frame):
        """
        YOLO에서 감지된 프레임을 직접 처리
        """
        try:
            print("compare_face_from_frame")
            # 임시 파일로 프레임 저장
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_path = temp_file.name
                cv2.imwrite(temp_path, frame)

            print("compare_face_from_frame suceess")
            # DeepFace로 얼굴 비교
            result = DeepFace.find(
                img_path=temp_path,
                db_path=self.db_path,
                detector_backend='retinaface',
                model_name='ArcFace'
            )

            # 임시 파일 삭제
            os.unlink(temp_path)

            # 결과 처리
            if result and not result[0].empty:
                distance = result[0]['distance'].iloc[0]
                is_match = distance <= self.threshold
                return is_match, distance
            
            return False, None

        except Exception as e:
            print(f"Face comparison error: {e}")
            return False, None