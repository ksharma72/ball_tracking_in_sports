import os
import shutil
import cv2
import numpy as np
from roboflow import Roboflow
from compress_video import compress_video
from extract_frames import extract_frames
from annotate_predictions import annotate_images, annotate_frames_with_speed
from create_video import create_video
from speed_calculations import calculate_windowed_speed


def cleanup(file_path, original_format):
    """
    Cleans up temporary files and folders created during the processing of an image or video file.

    Parameters:
    file_path (str): The path of the original file that was processed.
    original_format (str): The original file format (extension) of the processed file.

    This function removes temporary directories and files such as 'extracted_images',
    'annotated_images', and any temporary image or compressed video files. It handles both
    image and video formats and ensures that all temporary files created during processing
    are removed to free up space.
    """
    folders_to_remove = ['extracted_images', 'annotated_images']
    files_to_remove = []
    # For temporary files generated while processing an image
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        files_to_remove.append('temp_image.jpg')

    # For temporary files generated while processing a video
    if file_path.lower().endswith(('.mp4', '.mov')):
        files_to_remove.append('ffmpeg2pass-0.log')
        files_to_remove.append('ffmpeg2pass-0.log.mbtree')
        compressed_video_path = os.path.splitext(file_path)[0] + '_compressed' + original_format
        files_to_remove.append(compressed_video_path)

    # Remove the files and folders
    for folder in folders_to_remove:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    for file in files_to_remove:
        try:
            if os.path.exists(file):
                os.remove(file)
        except OSError as e:
            print(f"Error removing file {file}: {e}")
    print('Removed temporary files and folders -', folders_to_remove, files_to_remove)
    print("Cleanup complete.")


def process_file(file_path, roboflow_api_key):
    """
    Processes an image or video file for object detection using the Roboflow API.

    Parameters:
    file_path (str): The path of the file to be processed.
    roboflow_api_key (str): The API key for accessing the Roboflow service.

    The function first determines whether the file is an image or a video. For images, it applies
    a bilateral filter and then uses the Roboflow model for object detection, saving the annotated
    image. For videos, it compresses the video, extracts frames, annotates each frame, and then
    creates a new annotated video. The function also handles cleanup of temporary files after
    processing. Unsupported file formats will result in a printed message indicating the limitation.
    """
    original_format = None
    rf = Roboflow(api_key=roboflow_api_key)
    project = rf.workspace().project('tennis-tracker-duufq')
    model = project.version(15).model
    # Check if the file is an image or a video
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        # It's an image, so annotating it directly
        print("Processing image...")
        original_format = '.' + file_path.split('.')[-1]
        temp_image_path = "temp_image.jpg"
        image = cv2.imread(file_path)

        # Apply a bilateral filter to reduce noise while preserving edges
        filtered_image = cv2.bilateralFilter(image, 9, 25, 25)
        cv2.imwrite(temp_image_path, filtered_image)
        if not os.path.exists('outputs'):
            os.makedirs('outputs')
        model.predict(temp_image_path, confidence=40, overlap=30).save(f'outputs/image_annotated{original_format}')
        image = cv2.imread(f'outputs/image_annotated{original_format}')
        sharpening_kernel = np.array([[-1, -1, -1],
                                      [-1, 9, -1],
                                      [-1, -1, -1]])

        # Sharpen the annotated image
        sharpened_image = cv2.filter2D(image, -1, sharpening_kernel)
        cv2.imwrite(f'outputs/image_annotated{original_format}', sharpened_image)
        print("Image processed and saved as image_annotated.jpg")
    elif file_path.lower().endswith(('.mp4', '.mov')):
        # It's a video
        print("Processing video...")
        original_format = '.' + file_path.split('.')[-1]

        # Compressing the video
        compressed_video_path = compress_video(file_path, 2 * 1000, original_format)

        # Extracting frames from the video
        fps = extract_frames(compressed_video_path)

        # Annotating the extracted frames
        ball_positions = annotate_images(model)

        # Calculating ball speed
        ball_speeds = calculate_windowed_speed(ball_positions, fps, 10)

        # Annotating ball speed to each frame
        annotate_frames_with_speed(ball_speeds)

        # Creating a video from the annotated frames
        create_video(original_format, fps)
    else:
        print("Unsupported file format")

    # Cleanup temporary files and folders
    cleanup(file_path, original_format)
