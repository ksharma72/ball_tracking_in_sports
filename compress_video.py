import os
import ffmpeg


def compress_video(video_full_path, target_size, original_format):
    """
    Compresses a video to a specified target size using FFmpeg.

    Parameters:
    video_full_path (str): The path to the video file that needs to be compressed.
    target_size (int): The target size for the compressed video in kilobytes.
    original_format (str): The original format (file extension) of the video.

    This function compresses a video file to a target size while attempting to maintain
    quality. It handles both video and audio streams, ensuring the audio bitrate stays
    within a reasonable range. The function uses FFmpeg for two-pass encoding, which
    first analyses the video for optimal compression settings and then compresses the video
    accordingly. The function returns the path to the compressed video.

    Note:
    - The target size is an approximation and the final file size may vary.
    - Audio bitrate is adjusted to be within the range of 32kbps to 256kbps.
    - The function assumes FFmpeg is installed and accessible in the system's environment.
    """
    print(f"Compressing {video_full_path}...")
    compressed_video_full_path = video_full_path.split('.')[0] + '_compressed' + original_format
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    duration = float(probe['format']['duration'])

    # Finding the audio stream, if it exists
    audio_stream = next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)

    # If there is an audio stream, get the audio bitrate, otherwise set to 0.
    if audio_stream:
        audio_bitrate = float(audio_stream['bit_rate'])
        if audio_bitrate < min_audio_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    else:
        audio_bitrate = 0  # No audio stream

    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Adjusting video bitrate based on whether there's an audio track.
    video_bitrate = target_total_bitrate - audio_bitrate if audio_bitrate else target_total_bitrate

    # Setting up FFmpeg input
    i = ffmpeg.input(video_full_path)

    # Two-pass encoding
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}).overwrite_output().run()
    ffmpeg_output_params = {'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2}
    if audio_bitrate:
        ffmpeg_output_params.update({'c:a': 'aac', 'b:a': audio_bitrate})
    ffmpeg.output(i, compressed_video_full_path, **ffmpeg_output_params).overwrite_output().run()
    return compressed_video_full_path
