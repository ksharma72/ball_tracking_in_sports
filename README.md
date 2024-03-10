# Ball Tracking in Lawn Tennis using Deep Learning

This project provides a comprehensive solution for tracking tennis balls and players in images and videos using a pre-trained YOLOv5 model from Roboflow. It offers a command-line interface for easy processing of both images and videos.

## Features

- **Image Processing**: 
  - Apply bilateral filtering to reduce noise while preserving edges.
  - Annotate images with bounding boxes around tennis players and tennis balls using YOLOv8.
  - Sharpen annotated images for enhanced visual clarity.

- **Video Processing**: 
  - Compress videos using a lossless two-pass encoding algorithm supported by FFmpeg.
  - Extract frames, apply bilateral filtering, and annotate using YOLOv8.
  - Perform speed calculations for the tennis ball.
  - Interpolate positions for frames where the tennis ball is not detected.
  - Annotate frames with the calculated speed and recombine them into a video.
  - Display the speed of the tennis ball in pixels/second on the video.

## Usage

The project is accessible via a command-line interface provided by `script.py`.

### Running the Script

```bash
python3 script_name.py --path [file_path] --key [roboflow_api_key]
```

#### Arguments:

- `--path`: Specifies the file path of the image or video to be processed. Defaults to 'test_video.mov' if not provided.
- `--key`: Specifies the Roboflow API key required for processing the file. Defaults to 'dRSyJm9De3EpPn8Krg5w' if not provided.

### Obtaining Roboflow API Key

A unique Roboflow API key is required, which can be obtained by creating an account on [Roboflow](https://universe.roboflow.com). Alternatively, you can use the provided key: `dRSyJm9De3EpPn8Krg5w`.

## Installation
To set up the project, first ensure you have Python installed on your system. Then install the required libraries using the following command:
    
```bash
pip install -r requirements.txt
```

This project aims to offer an efficient and user-friendly way to track and analyze tennis gameplay, providing valuable insights for players, coaches, and enthusiasts.
