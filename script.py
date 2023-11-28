#!/usr/bin/env python3

import argparse
from main import process_file

"""
This script provides a command-line interface for tracking objects (like balls) in images or videos. 
It uses the `process_file` function from the `main` module, which requires the Roboflow API.

Usage:
    python3 script_name.py --path [file_path] --key [roboflow_api_key]

Arguments:
- --path: Specifies the file path of the image or video to be processed. 
          Default value is 'test_video.mov' if not provided.
- --key:  Specifies the Roboflow API key required for processing the file. 
          Default value is 'dRSyJm9De3EpPn8Krg5w' if not provided.

The script takes these arguments and passes them to the `process_file` function for object detection and tracking.
It's designed to be user-friendly and easily adaptable for different files and API keys.
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ball Tracking Command Line Script")
    parser.add_argument("--path", help="File path for input video/image", default="test_video.mov")
    parser.add_argument("--key", help="Your Roboflow API key", default="dRSyJm9De3EpPn8Krg5w")
    args = parser.parse_args()

    process_file(args.path, args.key)
