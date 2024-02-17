import subprocess
import os
from fetch_video import fetch_video

def extract_frames(video_path, id):
    output_folder = f"src/data/video_scene_images/{id}"

    # Check if the video file exists
    if not os.path.isfile(video_path):
        print("Video file does not exist.")
        return
    
    # Ensure the output directory exists, create if it does not
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder, exist_ok=True)

    # Get video duration in seconds
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 \"{video_path}\""
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    duration = float(result.stdout)

    # Calculate intervals for frame extraction
    intervals = duration / 9  # We want 10 frames, so we divide by 9 to get even intervals

    for i in range(10):
        # Calculate the timestamp for the current frame
        timestamp = intervals * i

        # Format the output frame file name
        frame_file = os.path.join(output_folder, f"frame_{i+1}.png")  # Save as PNG in the specified output folder

        # Build FFmpeg command for extracting the frame
        cmd = f"ffmpeg -ss {timestamp} -i \"{video_path}\" -frames:v 1 \"{frame_file}\" -y"
        subprocess.run(cmd, shell=True)

    print("Frames extraction completed.")


# Example usage
if __name__ == "__main__":
    video_path = "src/data/raw_videos/Face Your Biggest Fear To Win 800 000.mp4"  # Update this path to your video file
    id = 1  # Update this path to your desired output directory
    extract_frames(video_path, id)



