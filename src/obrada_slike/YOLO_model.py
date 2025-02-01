# Import the InferencePipeline object
from inference import InferencePipeline
import cv2
from PIL import Image 
import PIL

def my_sink(result, video_frame):
    if result.get("output_image"):  # Provjera da li postoji slika u rezultatu
        output_image = result["output_image"].numpy_image  # Numpy array

        if output_image is not None:
            # Prikaz slike
            cv2.imshow("Workflow Image", output_image)
            cv2.waitKey(1)

            # Čuvanje slike u output.jpg
            cv2.imwrite("output.jpg", output_image)

    print(result)  # Prikaz rezultata u terminalu
    

# initialize a pipeline object
pipeline = InferencePipeline.init_with_workflow(
    api_key="68uomVMA1kKCZEGjK0y4",
    workspace_name="projekt-r",
    workflow_id="detect-count-and-visualize-3",
    video_reference="vid5.mp4", # Path to video, device id (int, usually 0 for built in webcams), or RTSP stream url
    max_fps=30,
    on_prediction=my_sink
)
pipeline.start() #start the pipeline
pipeline.join() #wait for the pipeline thread to finish