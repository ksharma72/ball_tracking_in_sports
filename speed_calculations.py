import math
import numpy as np


def calculate_distance(pos1, pos2):
    """
    Calculate the Euclidean distance between two points.

    Parameters:
    pos1 (tuple): The first point as a (x, y) coordinate.
    pos2 (tuple): The second point as a (x, y) coordinate.

    Returns:
    float: The Euclidean distance between the two points.
    """
    return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)


def interpolate_position(prev_position, next_position, steps, step):
    """
    Interpolate a position between two points.

    Parameters:
    prev_position (tuple): The starting point for interpolation.
    next_position (tuple): The ending point for interpolation.
    steps (int): The total number of interpolation steps between the start and end points.
    step (int): The current step for which the position needs to be interpolated.

    Returns:
    tuple: The interpolated position for the given step.
    """
    delta_x = (next_position[0] - prev_position[0]) / (steps + 1)
    delta_y = (next_position[1] - prev_position[1]) / (steps + 1)
    return prev_position[0] + delta_x * step, prev_position[1] + delta_y * step


def smooth_positions(positions, window_size):
    """
    Smooth a sequence of positions using a moving average.

    Parameters:
    positions (list of tuples): A list of positions (x, y coordinates) to be smoothed.
    window_size (int): The size of the moving window used for averaging.

    Returns:
    list of tuples: The smoothed positions.
    """
    # Apply a simple moving average to smooth the positions
    smoothed_positions = []
    for i in range(len(positions)):
        start = max(0, i - window_size // 2)
        end = min(len(positions), i + window_size // 2 + 1)
        window_positions = [p for p in positions[start:end] if p is not None]
        if window_positions:
            avg_x = np.mean([p[0] for p in window_positions])
            avg_y = np.mean([p[1] for p in window_positions])
            smoothed_positions.append((avg_x, avg_y))
        else:
            smoothed_positions.append(None)
    return smoothed_positions


def calculate_windowed_speed(ball_positions, fps, window_size):
    """
    Calculate the speed of an object in each frame of a video.

    This function interpolates missing positions, applies smoothing, and calculates
    the speed for each frame based on the positions of the object.

    Parameters:
    ball_positions (list of tuples): The positions of the object in each frame.
    fps (float): The frame rate of the video.
    window_size (int): The size of the window used for smoothing positions.

    Returns:
    list of floats: The speed of the object in each frame.
    """
    # Interpolation for missing positions
    for i in range(1, len(ball_positions)):
        if ball_positions[i] is None and ball_positions[i - 1] is not None:
            for j in range(i + 1, len(ball_positions)):
                if ball_positions[j] is not None:
                    for k in range(i, j):
                        ball_positions[k] = interpolate_position(ball_positions[i - 1], ball_positions[j], j - i + 1,
                                                                 k - i + 1)
                    break

        # Smoothing positions
    smoothed_positions = smooth_positions(ball_positions, window_size)

    # Initialize speeds list
    speeds = [0] * len(ball_positions)
    time_interval = 1 / fps

    # Speed calculation for each frame
    for i in range(len(smoothed_positions) - 1):
        if smoothed_positions[i] and smoothed_positions[i + 1]:
            distance = calculate_distance(smoothed_positions[i], smoothed_positions[i + 1])
            speeds[i] = distance / time_interval
        else:
            speeds[i] = 0

    return speeds
