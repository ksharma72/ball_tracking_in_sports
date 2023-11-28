import os
import glob
import sys
import cv2
import numpy as np

import requests.exceptions


def annotate_images(model):
    """
    Annotates images in a specified folder using a given model for object detection, applies a sharpening filter,
    and extracts the positions of detected objects.

    This function processes each image in the 'extracted_images' folder, using the model to detect objects
    in the images. It particularly focuses on detecting and recording the positions of a specific object
    class, such as a tennis ball. After annotation, a sharpening filter is applied to enhance the visual
    clarity of the annotations. Annotated images are saved in the 'annotated_images' folder.

    The function also handles HTTP errors that may occur during API calls to the model for predictions.

    Parameters:
    model: A pre-trained model used for object detection. This model should have a `predict` method
            that takes an image file path and optional confidence and overlap parameters, and a `save` method
            to save the annotated image. It should also provide a `json` method to get the prediction results in JSON format.

    Returns:
    list of tuples: A list of positions (x, y) of the detected object (tennis ball) in each image. If the object
                    is not found in an image, `None` is appended to the list for that image.

    Notes:
    - The function assumes the existence of 'extracted_images' directory with images to process.
    - It creates an 'annotated_images' directory if it doesn't exist.
    - Sharpening is done using a predefined kernel suitable for general purposes.
    - HTTP errors during model API calls are caught and printed to the console.
    """
    image_folder = 'extracted_images'
    annotated_images = "annotated_images"
    ball_positions = []
    if not os.path.exists(annotated_images):
        os.makedirs(annotated_images)

    img_files = sorted(glob.glob(os.path.join(image_folder, '*')))

    # Return if no images are found
    if not img_files:
        print("No images found in the folder")
        return

    total_images = len(img_files)
    for index, img_file in enumerate(img_files):
        # Handle HTTP errors during API calls
        try:
            processed_image_path = os.path.join(annotated_images, os.path.basename(img_file))
            # Annotate the image and save it for each frame
            prediction = model.predict(img_file, confidence=40, overlap=30)
            prediction.save(processed_image_path)
            prediction_json = prediction.json()
            tennis_ball_found = False
            for prediction in prediction_json.get("predictions", []):
                if prediction["class"] == "tennis-ball":
                    x = prediction["x"]
                    y = prediction["y"]
                    ball_positions.append((x, y))
                    tennis_ball_found = True
                    break

            if not tennis_ball_found:
                ball_positions.append(None)

            image = cv2.imread(processed_image_path)

            # Sharpen the annotated image
            sharpening_kernel = np.array([[-1, -1, -1],
                                          [-1, 9, -1],
                                          [-1, -1, -1]])
            sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)
            cv2.imwrite(processed_image_path, sharpened_image)
            print(f"\rAnnotating images: {index + 1}/{total_images} ({(index + 1) / total_images * 100:.2f}%)", end='')
            sys.stdout.flush()
        except requests.exceptions.HTTPError as e:
            print("\nError with API call", e)
            continue
    print("\nAnnotation complete.")
    return ball_positions


def annotate_frames_with_speed(speeds):
    """
    Annotates a sequence of images with corresponding speed values.

    This function reads images from a specified folder, annotates each image with
    a speed value from the provided list, and saves the annotated images back to
    the same folder.

    Parameters:
    speeds (list of float): A list of speed values, where each speed corresponds to a frame.

    The function expects the images to be named in a sorted manner so that their
    alphabetical/numerical order corresponds to the chronological order of the frames.
    The speed values are annotated on the top-left corner of each image.

    Note:
    - The function assumes that the number of speed values matches the number of images.
    - Images are saved with the same filenames in the same folder, overwriting the original ones.
    """
    image_folder = "annotated_images"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (0, 0, 255)  # Red color
    line_type = 2

    img_files = sorted(glob.glob(os.path.join(image_folder, '*')))

    # Return if no images are found
    if not img_files:
        print("No images found in the folder")
        return

    total_images = len(img_files)
    for index, img_file in enumerate(img_files):
        processed_image_path = os.path.join(image_folder, os.path.basename(img_file))
        frame = cv2.imread(img_file)
        if index < len(speeds):
            speed_text = f"Speed: {speeds[index]:.2f} px/s"
            # Annotating the Speed of the ball to the frame
            cv2.putText(frame, speed_text, (10, 30), font, font_scale, font_color, line_type)
        cv2.imwrite(processed_image_path, frame)
        print(f"\rAnnotating images with speed: {index + 1}/{total_images} ({(index + 1) / total_images * 100:.2f}%)", end='')
        sys.stdout.flush()
    print("\nSpeed annotations complete.")