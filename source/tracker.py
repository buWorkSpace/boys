from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2

class ObjectTracker:
    def __init__(self, max_age=50):
        self.tracker = DeepSort(max_age=max_age)

    def update(self, detections, frame):
        # DeepSort를 사용하여 객체 추적 업데이트
        tracks = self.tracker.update_tracks(detections, frame=frame)
        return tracks

    def print_tracks(self, tracks, frame):
        for track in tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_ltwh()  # [top_left_x, top_left_y, width, height]

            x1, y1, w, h = map(int, bbox)

            # track의 ID로 클래스 이름 설정
            class_id = track.class_id if hasattr(track, 'class_id') else -1
            class_name = "Unknown"  # 클래스 이름 가져오기

            # 바운딩 박스 및 클래스 이름 그리기
            cv2.rectangle(frame, (x1, y1), (w, h), (0, 255, 0), 2)  # ltrb 형식으로 그리기
            label = f'{class_name} {track.track_id}'
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame