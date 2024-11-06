import cv2
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from deepface import DeepFace
import pandas as pd

class FaceRecognition:
    def __init__(self, font_path="/usr/share/fonts/truetype/nanum/NanumGothic.ttf"):
        # Load Korean font for visualization
        plt.rc('font', family='NanumGothic')
        self.fontprop = font_manager.FontProperties(fname=font_path)
    
    def load_image(self, img_path):
        # Load image from path
        return cv2.imread(img_path)

    def find_match(self, img_path, db_path, detector_backend='retinaface', model_name='ArcFace', threshold=0.5):
        """
        Finds a match for the given image in the specified database.
        
        Parameters:
            img_path (str): Path to the image for recognition.
            db_path (str): Path to the database of face images.
            detector_backend (str): Face detector backend to use.
            model_name (str): DeepFace model name to use.
            threshold (float): Threshold for matching.
        
        Returns:
            dict: Contains match status, distance, and path to the matched image.
        """
        try:
            # Perform face recognition
            result = DeepFace.find(img_path=img_path, db_path=db_path,
                                   detector_backend=detector_backend, model_name=model_name)
            
            # Extract result if a match is found
            if result and not result[0].empty:
                df = result[0]
                distance = df['distance'].iloc[0]
                is_match = distance <= threshold
                match_info = {
                    "is_match": is_match,
                    "distance": distance,
                    "matched_image": df['identity'].iloc[0] if is_match else None
                }
            else:
                # No match found
                match_info = {"is_match": False, "distance": None, "matched_image": None}
            return match_info

        except Exception as e:
            print("An error occurred:", e)
            return None

    def visualize_results(self, img_path, match_info):
        """
        Visualizes the original and matched images, and displays match status.
        
        Parameters:
            img_path (str): Path to the original image.
            match_info (dict): Information about the match result.
        """
        # Load input image
        img = self.load_image(img_path)
        
        if match_info and match_info["is_match"]:
            # Matched image found, display side-by-side
            fig, axes = plt.subplots(1, 2, figsize=(10, 5))
            axes[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            axes[0].axis("off")
            
            # Load matched image
            res_img = self.load_image(match_info["matched_image"])
            axes[1].imshow(cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB))
            axes[1].axis("off")
            
            # Title with match status
            title_text = f"등록된 회원입니다. Match: {match_info['is_match']}"
            plt.suptitle(title_text, fontproperties=self.fontprop)
            plt.show()

        else:
            # No matching faces found
            print("No matching faces found in the database.")
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            plt.axis("off")
            plt.title("미등록 회원입니다.", fontproperties=self.fontprop)
            plt.show()

# Usage
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # Adjust as needed for your system
face_recognition = FaceRecognition(font_path=font_path)

img_path = '/content/drive/MyDrive/Colab Notebooks/deepface_img/test2.jpg'
db_path = '/content/drive/MyDrive/Colab Notebooks/member_img'

match_info = face_recognition.find_match(img_path=img_path, db_path=db_path)
face_recognition.visualize_results(img_path=img_path, match_info=match_info)
