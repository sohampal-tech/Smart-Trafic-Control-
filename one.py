from flask import Flask, render_template, request, jsonify
import os
from SMART_TRAFFIC_DETECTION_3 import process_video  # Ensure this imports correctly

app = Flask(_name_)

# Configure upload folder
UPLOAD_FOLDER = r'C:\Users\user\Downloads\DSA_PROJECT\HTML_VIDEO_UPLOADS'  # Correct path with raw string
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('SMART_TRAFFIC_DETECTION.html')

@app.route('/process-video', methods=['POST'])
def process_video_route():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided."}), 400

    video = request.files['video']
    if video.filename == '':
        return jsonify({"error": "No selected file."}), 400

    # Save the video to the upload folder
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video.filename)
    video.save(video_path)

    # Call the vehicle detection function
    try:
        results = process_video(video_path)  # Ensure process_video returns JSON-serializable data
    except Exception as e:
        return jsonify({"error": f"Error processing video: {str(e)}"}), 500

    return jsonify(results)

if _name_ == '_main_':
    app.run(debug=True)