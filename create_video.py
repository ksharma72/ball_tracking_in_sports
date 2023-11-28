import imageio
import os
import sys


def create_video(original_format, fps=30):
    """
    Creates a video from a sequence of annotated images stored in a specified folder.

    Parameters:
    original_format (str): The file extension for the output video file.
    fps (int, optional): Frames per second for the output video. Defaults to 30.

    The function compiles images from the 'annotated_images' folder into a video file.
    It expects the images to be in a format suitable for video creation (like .jpg, .png,
    or .jpeg) and sorts them if they are named sequentially. The created video is saved
    in the 'outputs' directory with the specified original format. The function provides
    real-time progress updates in the console during video creation.

    Note:
    - The function creates an 'outputs' directory if it doesn't already exist.
    - If there are no images in the 'annotated_images' folder, the function will terminate
      without creating a video.
    - The function relies on the `imageio` library for reading images and creating the video.
    """
    output_video = 'output_video' + original_format
    image_folder = 'annotated_images'
    # Getting all image files in the folder
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png") or img.endswith(".jpeg")]
    # Sorting the images if they are named sequentially
    images.sort()

    total_images = len(images)

    # Return if no images are found
    if total_images == 0:
        return

    # Creating the outputs folder if it doesn't exist
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    # Creating the video
    with imageio.get_writer(f'outputs/{output_video}', fps=fps) as writer:
        for index, image in enumerate(images):
            img_path = os.path.join(image_folder, image)

            # Updating and displaying the progress
            print(f"\rAdding image to video: {index + 1}/{total_images} ({(index + 1) / total_images * 100:.2f}%)",
                  end='')
            sys.stdout.flush()

            image_data = imageio.imread(img_path)
            writer.append_data(image_data)

    print("\nVideo creation complete. Video saved as", output_video)
