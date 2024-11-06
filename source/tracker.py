from deep_sort_realtime.deepsort_tracker import DeepSort

class ObjectTracker:
    def __init__(self, max_age=50):
        self.tracker = DeepSort(max_age=max_age)

    def update(self, detections, frame):
        tracks = self.tracker.update_tracks(detections, frame=frame)
        return tracks

    def print_tracks(self, tracks, frame):
        for track in tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue