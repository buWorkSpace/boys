import torch
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        result = torch.backends.mps.is_available()
        print(f'MPS is available: {result}')
        if result:
            self.model.to('mps')

    def detect_objects(self, frame):
        results = self.model(frame)
        detections = []

        if len(results):
            for result in results:
                for *xyxy, conf, cls in result.boxes.data.tolist():
                    box = [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])]
                    detections.append((box, conf, int(cls)))

        return detections

