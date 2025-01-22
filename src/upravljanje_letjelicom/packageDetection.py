from ultralytics import YOLO
from djitellopy import Tello
import cv2

# Path to the custom or pretrained YOLO model
MODEL_PATH = './yolo11s.pt'  # Path to the locally saved YOLO weights

def detect_packages_with_drone():
    """
    Detect packages using the drone's video feed with YOLOv11 locally.
    """
    # Connect to the drone
    drone = Tello()
    drone.connect()
    print(f"Battery level: {drone.get_battery()}%")

    # Start the drone's video stream
    drone.streamon()

    # Load the YOLO model
    print("Loading YOLOv11 model locally...")
    model = YOLO(MODEL_PATH)  # Load the YOLO model locally

    print("Press 'q' to quit.")
    try:
        while True:
            # Get a frame from the drone's video feed
            frame = drone.get_frame_read().frame

            # Perform YOLO detection
            results = model.predict(frame, conf=0.5)

            # Parse and draw detections
            for result in results:
                for box in result.boxes.xyxy.cpu().numpy():
                    x1, y1, x2, y2 = box[:4]
                    conf = box[4]  # Confidence score
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, f"Package {conf:.2f}", (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display the number of detected packages
            num_packages = len(results[0].boxes)
            cv2.putText(frame, f"Packages detected: {num_packages}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Show the frame with detections
            cv2.imshow('Drone Package Detection', frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Landing the drone...")
        drone.land()
    finally:
        # Stop the video stream and close all windows
        drone.streamoff()
        cv2.destroyAllWindows()
        print("Video feed closed.")

if __name__ == "__main__":
    detect_packages_with_drone()
