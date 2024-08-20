from moviepy.editor import VideoFileClip
import cv2
import os

def extract_frames(video_path, output_dir, fps=1):
    """Extract frames from the video using moviepy and OpenCV."""
    clip = VideoFileClip(video_path)
    os.makedirs(output_dir, exist_ok=True)
    for i, frame in enumerate(clip.iter_frames(fps=fps)):
        frame_path = os.path.join(output_dir, f"frame_{i}.jpg")
        cv2.imwrite(frame_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    clip.reader.close()
