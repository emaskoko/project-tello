from inference import InferencePipeline
import cv2
import numpy as np
from dotenv import load_dotenv
import os


tracked_boxes = []  # Lista za praćenje bounding boxeva
package_count = 0   # Broj ukupno detektovanih paketa

def yolo_count(drone_video: str):
    # Učitavanje API ključa iz .env fajla
    load_dotenv()
    API_KEY = os.getenv("API_KEY")

    # Globalne promenljive

    # Prag za preklapanje (Intersection over Union - IoU)
    IOU_THRESHOLD = 0.1

    # Funkcija za izračunavanje IoU između dva bounding boxa
    def calculate_iou(box1, box2):
        x1, y1, x2, y2 = box1
        x1_p, y1_p, x2_p, y2_p = box2

        # Koordinate preseka
        xi1 = max(x1, x1_p)
        yi1 = max(y1, y1_p)
        xi2 = min(x2, x2_p)
        yi2 = min(y2, y2_p)

        # Površina preseka
        inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

        # Površina oba pravougaonika
        box1_area = (x2 - x1) * (y2 - y1)
        box2_area = (x2_p - x1_p) * (y2_p - y1_p)

        # Izračunavanje IoU
        iou = inter_area / float(box1_area + box2_area - inter_area)
        return iou

    # Funkcija za obradu detekcija
    def my_sink(result, video_frame):
        global tracked_boxes, package_count

        # Prikaz slike
        if result.get("output_image"):
            output_image = result["output_image"].numpy_image
            cv2.imshow("Workflow Image", output_image)
            cv2.waitKey(1)
            cv2.imwrite("outputSlika.jpg", output_image)

        # Provera da li postoje detekcije
        if result.get("predictions"):
            detections = result["predictions"].xyxy  # Koordinate bounding boxeva

            for box in detections:
                x1, y1, x2, y2 = box.astype(int)

                # Provera da li je ovo novi paket (nema značajno preklapanje sa postojećim)
                is_new_package = True
                for tracked_box in tracked_boxes:
                    if calculate_iou((x1, y1, x2, y2), tracked_box) > IOU_THRESHOLD:
                        is_new_package = False
                        break

                if is_new_package:
                    tracked_boxes.append((x1, y1, x2, y2))  # Dodavanje novog paketa u praćenje
                    package_count += 1
                    print(f"📦 Novi paket detektiran! Ukupno: {package_count}")

    # Inicijalizacija pipeline-a
    pipeline = InferencePipeline.init_with_workflow(
        api_key=API_KEY,
        workspace_name="projekt-r",
        workflow_id="detect-count-and-visualize-3",
        video_reference=drone_video,
        max_fps=30,
        on_prediction=my_sink
    )

    pipeline.start()
    pipeline.join()

    print(f"Ukupno detektiranih paketa: {package_count}")
    return package_count

# yolo_count('../video.avi')
