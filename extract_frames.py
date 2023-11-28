import cv2
import os
import sys


def extract_frames(video_path):
    """
    Extracts frames from a given video file and applies a bilateral filter to each frame.

    Parameters:
    video_path (str): The path to the video file from which frames will be extracted.

    This function opens a video file, calculates its frames per second (FPS), and then
    iteratively extracts each frame, applying a bilateral filter to reduce noise while
    preserving edges. Extracted frames are saved in the 'extracted_images' folder,
    named sequentially. The function provides real-time progress updates in the console.
    It returns the FPS of the original video, which can be useful for further processing
    like video reconstruction.

    Note:
    - The function creates an 'extracted_images' directory if it doesn't already exist.
    - It assumes that OpenCV is installed and properly configured.
    - If the video file cannot be opened, the function will print an error message.
    """
    output_folder = 'extracted_images'
    # Creating the extracted_images folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Opening the video file
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    if not cap.isOpened():
        print("Error opening video file")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_count = 0
    while True:
        success, frame = cap.read()

        # Breaking the loop if read was not successful
        if not success:
            break

        # Applying bilateral filter to each frame
        filtered_image = cv2.bilateralFilter(frame, 9, 25, 25)

        frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, filtered_image)

        # Updating progress
        frame_count += 1
        progress = (frame_count / total_frames) * 100
        print(f"\rExtracting frames: {frame_count}/{total_frames} frames ({progress:.2f}%)", end='')

        # Flushing the output to ensure it updates in real time
        sys.stdout.flush()

    # Releasing the video capture object
    cap.release()
    print(f"\nExtracted {frame_count} frames")
    return fps
