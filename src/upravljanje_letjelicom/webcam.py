from ultralytics import YOLO
import cv2

# Path to the YOLOv11 model weights
MODEL_PATH = 'yolo11s.pt'  # Replace with your local model path

def detect_objects_webcam():
    """
    Perform real-time object detection using YOLOv11 on a webcam.
    """
    # Load the YOLO model
    print("Loading YOLOv11 model...")
    model = YOLO(MODEL_PATH)

    # Open webcam (camera index 0 is the default webcam)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'q' to quit.")
    try:
        while True:
            # Capture a frame from the webcam
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            # Perform YOLO detection
            results = model.predict(frame, conf=0.5)  # Adjust confidence threshold if needed

            # Draw bounding boxes and labels on the frame
            for result in results:
                for box in result.boxes:
                    # Extract bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].tolist()

                    # Extract confidence score
                    conf = box.conf[0].item() if box.conf is not None else 0.0

                    # Extract class label index
                    cls = int(box.cls[0].item()) if box.cls is not None else -1

                    # Get label name (if available)
                    label = model.names[cls] if cls != -1 else "Unknown"

                    # Draw bounding box
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} {conf:.2f}", (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display the frame with detections in a live feed
            cv2.imshow('YOLOv11 Live Detection Feed', frame)

            # Quit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release webcam and close windows
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam closed.")

if __name__ == "__main__":
    detect_objects_webcam()
