from flask import Flask, request
import cv2
import numpy as np
from deepface import DeepFace
import tempfile
import os

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return "No image uploaded", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
        file.save(temp.name)
        temp_path = temp.name

    try:
        # Read image with OpenCV
        img = cv2.imread(temp_path)
        if img is None:
            return "Invalid image", 400

        # Use DeepFace to analyze emotion
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion'] if isinstance(result, list) else result['dominant_emotion']

        return dominant_emotion  # Return as plain text

    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        os.remove(temp_path)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
