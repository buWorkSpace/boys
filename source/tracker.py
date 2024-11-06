from deep_sort_realtime.deepsort_tracker import DeepSort
from deep_sort_realtime.deep_sort.track import Track as DeepSORTTrack
import cv2
import os
from datetime import datetime
from source.face_recognition import FaceRecognition


class CustomTrack(DeepSORTTrack):
    def __init__(self, mean, covariance, track_id, n_init, max_age, feature=None, original_ltwh=None, det_class=None, det_conf=None, instance_mask=None, others=None):  
        super().__init__(mean, covariance, track_id, n_init, max_age, feature)
        self.is_member = False
        self.last_check_age = -1
        # self.original_ltwh = original_ltwh
        # self.det_class = det_class

    def update_member_status(self, is_member):
        self.is_member = is_member
        self.last_check_age = self.age


class ObjectTracker(DeepSort):
    def __init__(self, max_age=50):
        self.tracker = DeepSort(max_age=max_age, override_track_class=CustomTrack)
        self.face_recognizer = FaceRecognition()  # FaceRecognition 인스턴스 생성

        # 얼굴 이미지 저장 폴더 생성, 삭제해도 됨
        self.check_face_dir = "./checkFaceFolder"
        os.makedirs(self.check_face_dir, exist_ok=True)

    def update(self, detections, frame):
        # DeepSort를 사용하여 객체 추적 업데이트
        tracks = self.tracker.update_tracks(detections, frame=frame)
        return tracks

    def print_tracks(self, tracks, frame):
        for track in tracks:
            if not track.is_confirmed():
                continue
            bbox = track.to_ltwh()  # [top_left_x, top_left_y, width, height]
            
            # 얼굴 영역 좌표
            x1, y1, w, h = map(int, bbox)
            

            # 멤버 상태 체크 및 업데이트
            if (track.last_check_age == -1 or (track.age - track.last_check_age) > 30) and not track.is_member:
                # 얼굴 영역 추출
                face_img = frame[y1:h, x1:w]  
               
                # 이미지가 비어있지 않은지 확인
                if face_img.size > 0:  
                    # 얼굴 이미지 저장
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"face_id{track.track_id}_{timestamp}.jpg"
                    save_path = os.path.join(self.check_face_dir, filename)
                    cv2.imwrite(save_path, face_img)

                    # 인식 시간으로 인한 딜레이 발생-> 비동기로 처리해서 실시간 보장해보기
                    is_match, _ = self.face_recognizer.compare_face_from_frame(face_img)
                    track.update_member_status(is_match)
            

            # 인스턴스 메서드로 호출
            # is_match, distance = self.face_recognizer.compare_face_from_frame(face_img)
            
            # # 결과 표시
            # color = (0, 255, 0) if is_match else (0, 0, 255)
            # label = f"Member" if is_match else "Unknown"
            # cv2.rectangle(frame, (x1, y1), (x1+w, y1+h), color, 2)
            # cv2.putText(frame, label, (x1, y1-10), 
            #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # track의 ID로 클래스 이름 설정
            # class_id = track.class_id if hasattr(track, 'class_id') else -1
            class_name = "Unknown"  # 클래스 이름 가져오기

            # 멤버 상태에 따른 색상 및 라벨 설정
            color = (0, 255, 0) if track.is_member else (0, 0, 255)  # 멤버면 초록색, 아니면 빨간색
            status = "Member" if track.is_member else "Unknown"
            label = f'{status} {track.track_id}'
            cv2.rectangle(frame, (x1, y1), (w, h), color, 2)  # ltrb 형식으로 그리기
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return frame