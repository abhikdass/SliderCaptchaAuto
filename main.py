from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import random
from datetime import datetime, timedelta

app = Flask(__name__)

def decode_base64_image(b64_string):
    """
    Decodes a base64 image into a numpy array.
    """
    img_data = base64.b64decode(b64_string)
    img_array = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)

def find_slider_position(background, slider):
    """
    Finds the position of the slider image that fits in the background.
    """
    background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    slider_gray = cv2.cvtColor(slider, cv2.COLOR_BGRA2GRAY) if slider.shape[-1] == 4 else cv2.cvtColor(slider, cv2.COLOR_BGR2GRAY)
    _, slider_mask = cv2.threshold(slider_gray, 1, 255, cv2.THRESH_BINARY)
    result = cv2.matchTemplate(background_gray, slider_gray, cv2.TM_CCOEFF_NORMED, mask=slider_mask)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    return max_loc

def generate_tracks(target_distance, total_time):
    """
    Generate simulated tracks for a slider to move a specified distance over time.
    """
    tracks = []
    current_x = 0
    current_time = 0
    while current_x < target_distance:
        step = random.randint(5, 15)
        step_time = random.randint(10, 50)
        current_x = min(current_x + step, target_distance)
        current_time += step_time
        y_variation = random.randint(-3, 3)
        tracks.append({"x": current_x, "y": y_variation, "t": current_time})
    for _ in range(5):
        current_time += random.randint(10, 50)
        tracks.append({"x": target_distance, "y": 0, "t": current_time})
    return tracks

@app.route('/generate-tracks', methods=['POST'])
def generate_slider_tracks():
    """
    API endpoint to generate tracks for slider verification.
    """
    try:
        # Get data from the request
        data = request.json
        background_b64 = data.get("bgbase64image")
        slider_b64 = data.get("sliderbase64image")
        total_time = data.get("total_time", 1000)  # Default to 1000 ms

        # Decode base64 images
        background_img = decode_base64_image(background_b64)
        slider_img = decode_base64_image(slider_b64)

        # Find slider position
        match_position = find_slider_position(background_img, slider_img)

        # Generate tracks for the movement
        tracks = generate_tracks(match_position[0], total_time)

        # Generate timestamps
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(milliseconds=total_time)

        # Build the response
        result = {
            "backgroundImageWidth": background_img.shape[1],
            "backgroundImageHeight": background_img.shape[0],
            "sliderImageWidth": slider_img.shape[1],
            "sliderImageHeight": slider_img.shape[0],
            "startTime": start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "endTime": end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "tracks": tracks,
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True,port=5050)
