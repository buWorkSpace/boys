import cv2
import time  # FPS 계산을 위한 time 모듈 추가
from source.detector import ObjectDetector
from source.tracker import ObjectTracker
# from face_recognition import FaceRecognition

class VideoSaver:
    def __init__(self, input_path, output_path):
        self.cap = cv2.VideoCapture(input_path)
        if not self.cap.isOpened():
            print('Error opening video file')
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(output_path, fourcc, self.fps, (width, height))

    def write_frame(self, frame):
        self.out.write(frame)

    def release(self):
        self.cap.release()
        self.out.release()


class FPSCounter:
    def __init__(self):
        self.prev_frame_time = 0
        self.fps = 0

    def update(self):
        new_frame_time = time.time()  # 현재 시간 가져오기
        self.fps = 1 / (new_frame_time - self.prev_frame_time)
        self.prev_frame_time = new_frame_time
        return int(self.fps)

def main():
    print('start')

    # M1 Mac에서 MPS 백엔드 사용
    model = ObjectDetector('./model/yolov8n-face.pt')
    tracker = ObjectTracker(max_age=50)

    # 웹캠 설정 변경
    cap = cv2.VideoCapture(0)  # 또는 cv2.CAP_AVFOUNDATION + 0
    
    # 웹캠 설정
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
    
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다")
        return

    # output_video_path = 'output_video.mp4'
    
    # VideoSaver 수정된 초기화
    # video_saver = VideoSaver(0, output_video_path)
    fps_counter = FPSCounter()

    while True:
        ret, frame = cap.read()
        
        # 프레임 유효성 강화된 검사
        if not ret or frame is None or frame.size == 0:
            print("프레임 읽기 실패, 재시도...")
            continue

        detections = model.detect_objects(frame)
        tracks = tracker.update(detections, frame)
        frame = tracker.print_tracks(tracks, frame)
            
        fps = fps_counter.update()
        cv2.putText(frame, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2)
            
        cv2.imshow('Face Detection', frame)
        # video_saver.write_frame(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    # video_saver.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()




# https://github.com/derronqi/yolov8-face - yolov8n 출처