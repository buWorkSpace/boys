import cv2
import time  # FPS 계산을 위한 time 모듈 추가
from source.detector import ObjectDetector
from source.tracker import ObjectTracker

class VideoSaver:
    def __init__(self, input_path, output_path):
        self.cap = cv2.VideoCapture(input_path)
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


	# def main():
	# YOLOv8 모델 및 DeepSort 초기화
	model = ObjectDetector('/content/drive/MyDrive/Colab Notebooks/yolov8n-face.pt')
	tracker = ObjectTracker(max_age=50)

	# 비디오 파일 경로 및 설정
	input_video_path = '/content/drive/MyDrive/Colab Notebooks/faceCam영상.mov'
	output_video_path = 'output_video.mp4'

	# VideoSaver 초기화
	video_saver = VideoSaver(input_video_path, output_video_path)

	# FPSCounter 초기화
	fps_counter = FPSCounter()

	while video_saver.cap.isOpened():
		ret, frame = video_saver.cap.read()
		if not ret:
			break

		# 객체 감지 수행
		detections = model.detect_objects(frame)

		# 객체 추적 업데이트
		tracks = tracker.update(detections, frame)

		# 추적된 객체에 대해 바운딩 박스 및 클래스 이름 그리기
		frame = tracker.print_tracks(tracks, frame)

		# FPS 계산 및 텍스트 추가
		fps = fps_counter.update()
		
		# 프레임에 FPS 텍스트 추가
		cv2.putText(frame, str(fps), (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
		
		# 프레임을 출력 비디오에 저장
		video_saver.write_frame(frame)

	# 리소스 해제
	video_saver.release()
	cv2.destroyAllWindows()

	# if __name__ == "__main__":
		# main()

	# https://github.com/derronqi/yolov8-face - yolov8n 출처