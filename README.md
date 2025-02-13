# Slider Position Detection and Track Generation

## Overview
This Python script detects the position of a slider on a background image and generates movement tracks for it. The images are provided as Base64-encoded strings, and the script processes them using OpenCV and NumPy. It is useful for CAPTCHA solving automation where a slider needs to be moved to match a background position.

## Features
- Decodes Base64-encoded images.
- Converts images to grayscale for processing.
- Uses OpenCV's `matchTemplate` to find the slider position.
- Generates movement tracks with random variations.
- Outputs the result in a structured format, including timestamps.

## Prerequisites
Ensure you have the required Python libraries installed:

```bash
pip install numpy opencv-python
```

## Usage
### 1. Prepare Base64 Images
- Save the Base64-encoded background image in `background.txt`.
- Save the Base64-encoded slider image in `slider.txt`.

### 2. Run the Script
Execute the script using Python:

```bash
python main.py
```

### 3. Expected Output
The script will return a JSON-like dictionary containing:
- Background and slider image dimensions.
- Start and end timestamps.
- Generated movement tracks.

Example Output:

```json
{
  "backgroundImageWidth": 300,
  "backgroundImageHeight": 150,
  "sliderImageWidth": 50,
  "sliderImageHeight": 50,
  "startTime": "2025-02-13T12:00:00.000Z",
  "endTime": "2025-02-13T12:00:01.000Z",
  "tracks": [
    {"x": 10, "y": 1, "t": 20},
    {"x": 25, "y": -2, "t": 50},
    ...
  ]
}
```

## Functions Explained
### `decode_base64_image(b64_string)`
Decodes a Base64-encoded image and converts it into an OpenCV-readable format.

### `find_slider_position(background, slider)`
Finds the best matching position of the slider in the background image using `cv2.matchTemplate`.

### `generate_tracks(target_distance, total_time)`
Generates a list of track points simulating human-like slider movement.

### `generate_slider_tracks(background_b64, slider_b64, total_time=1000)`
Main function that integrates all steps and returns the final result.

## Notes
- Ensure the images are properly formatted before encoding to Base64.
- The script introduces randomness in track generation to mimic human behavior.

## License
This script is provided under the MIT License.

