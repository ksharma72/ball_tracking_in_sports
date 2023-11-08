import cv2
import numpy as np

def contoursDetection(image):
    # Load the image
    #cv2.imshow("Original Image", image)
    #cv2.waitKey(0)
    # Convert the image to grayscale
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Gray Image", gray)
    # cv2.waitKey(0)
    #Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(image, (11, 11), 0)
    # cv2.imshow("Blur Image", blurred)
    # cv2.waitKey(0)

    # Define the lower and upper bounds for the yellow color in HSV
    lower_yellow = np.array([25, 100, 100], dtype="uint8")
    upper_yellow = np.array([30, 255, 255], dtype="uint8")

    # Convert the image to HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    #cv2.imshow("HSV Image", hsv)
    #cv2.waitKey(0)

    # Create a mask for the yellow color
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #cv2.imshow("Yellow Mask Image", yellow_mask)
    #cv2.waitKey(0)


    binary_image = cv2.threshold(yellow_mask, 128, 255, cv2.THRESH_BINARY)[1]
    #cv2.imshow("Binary Image", binary_image)
    #cv2.waitKey(0)


    # Find contours in the yellow mask
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0,255,0), 3)

    # Filter and draw bounding boxes around circular contours
    # for contour in contours:
    #     # Calculate the area and perimeter of the contour
    #     area = cv2.contourArea(contour)
    #     perimeter = cv2.arcLength(contour, True)
    #     print("Area: ", area)
    #     print("Perimeter: ", perimeter)
    #
    #     if area == 0 and perimeter == 0:
    #         continue
    #     # Calculate circularity
    #     circularity = 4 * np.pi * area / (perimeter ** 2)
    #     print("Circularity: ", circularity)
    #
    #     # Filter based on area and circularity
    #     if area > 1000:# and 0.7 < circularity < 1.3:
    #         # Draw a bounding box around the contour
    #         x, y, w, h = cv2.boundingRect(contour)
    #         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the image with bounding boxes
    cv2.imshow('Tennis Ball Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return image


tennisVideo = cv2.VideoCapture('test_video.mov')

fps = int(tennisVideo.get(cv2.CAP_PROP_FPS))
width = int(tennisVideo.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(tennisVideo.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
outputVideo = cv2.VideoWriter('./OutputWimbledonVideo.mp4', fourcc, fps, (width, height), isColor=True)

framesRead = 0
while (framesRead <= 1000):
    print("reading frame - ", framesRead)
    ret, frame = tennisVideo.read()
    if not ret:
        break
    
    cFrame = contoursDetection(frame)
    outputVideo.write(cFrame)
    framesRead += 1
framesRead = 0

# Release the video ballVideoture
tennisVideo.release()
