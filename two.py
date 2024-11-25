import cv2
import numpy as npin

def process_video(video_path):
    # Paths to YOLO files
    weights_path = r"C:\Users\user\Downloads\yolov4.weights"  # Use raw string
    cfg_path = r"C:\Users\user\Downloads\DSA_PROJECT\yolov4.cfg"
    names_path = r"C:\Users\user\Downloads\DSA_PROJECT\coco.names"

    # Check if files exist
    for path in [weights_path, cfg_path, names_path]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found!")

    # Load YOLO model
    net = cv2.dnn.readNet(weights_path, cfg_path)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    # Load class names
    with open(names_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # Initialize counts
    counts = {"car": 0, "truck": 0, "bus": 0, "motorbike": 0, "total": 0}

    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Error opening video file.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outputs = net.forward(output_layers)

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and classes[class_id] in counts:
                    counts[classes[class_id]] += 1
                    counts["total"] += 1

    cap.release()
    return counts