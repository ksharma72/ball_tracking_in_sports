import os
import cv2
import shutil


def copy_folder(data_labels_path, processed_data_labels_path):
    try:
        shutil.copytree(data_labels_path, processed_data_labels_path)
        print(f"Folder '{data_labels_path}' copied to '{processed_data_labels_path}' successfully.")
    except shutil.Error as e:
        print(f"Error: {e}")
    except OSError as e:
        print(f"Error: {e}")


def remove_noise(folders, data_path, processed_data_path):
    for folder in folders:
        if os.path.isdir(os.path.join(data_path, folder)):
            for image in os.listdir(os.path.join(data_path, folder)):
                image_path = os.path.join(data_path, folder, image)
                input_image = cv2.imread(image_path)
                if input_image is not None:
                    processed_image = cv2.medianBlur(input_image, 5)

                    # Create the destination folder if it doesn't exist
                    if not os.path.exists(processed_data_path):
                        os.makedirs(processed_data_path)
                    if not os.path.exists(os.path.join(processed_data_path, folder)):
                        os.makedirs(os.path.join(processed_data_path, folder))
                    destination_path = os.path.join(processed_data_path, folder, image)
                    cv2.imwrite(destination_path, processed_image)


if __name__ == "__main__":
    data_images_path = '/Users/sujith/Desktop/data/images'
    processed_data_images_path = '/Users/sujith/Desktop/processed_data/images'
    folders = os.listdir(data_images_path)
    data_labels_path = '/Users/sujith/Desktop/data/labels'
    processed_data_labels_path = '/Users/sujith/Desktop/processed_data/labels'
    remove_noise(folders, data_images_path, processed_data_images_path)
    copy_folder(data_labels_path, processed_data_labels_path)
