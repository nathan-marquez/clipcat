from get_info import get_info
from chunk_text import chunk_text
from cluster_videos import cluster_videos
from extract_scenes import extract_scenes
from get_summary import get_summary
from get_transcript import get_transcript
from fetch_video import fetch_video
from create_scene_caption import generate_captions_for_folder
import json
import os
from pytube import YouTube
import scrapetube

# Folder to save the JSON files
folder_path = "src/data/video_documents"

# Ensure the folder exists
os.makedirs(folder_path, exist_ok=True)

# Your list of YouTube video URLs
urls = []
videos = scrapetube.get_channel("UCX6OQ3DkcsbYNE6H8uQQuVA")
count = 0
for video in videos:
    count += 1
    if count > 100:
        break
    if count < 38: continue
    videoId = video['videoId']
    urls.append(f'https://www.youtube.com/watch?v={videoId}')
    
# Function to save a URL to a JSON file
def save_url_to_json(url, folder_path, id):
    file_path = os.path.join(folder_path, f"video{id}.json")
    
    YouTube(url).streams.first().download(output_path = 'src/data/raw_videos_full', filename ='currentvid.mp4')

    video_path = 'src/data/raw_videos_full/currentvid.mp4'

    extract_scenes(video_path, id)

    video_info = get_info(url)
    print("got info")
    video_transcript = get_transcript(url)
    print("got transcript")

    video_transcript_chunks = chunk_text(video_transcript)
    print("got video_transcript_chunks")

    video_summary = get_summary(video_transcript)
    print("got video_summary")

    video_scene_captions = generate_captions_for_folder(f"src/data/video_scene_images/{id}")
    print("got video_scene_captions")


    # Create a dictionary with the URL
    url_dict = {"url": url,
                "trascript_chunks": video_transcript_chunks,
                "summary": video_summary,
                "scene_captions": video_scene_captions
                }
    
    url_dict.update(video_info)
    
    # Save the dictionary to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(url_dict, json_file, indent=4)
    
    print(f"URL saved to {file_path}")

    os.remove(video_path)


# Iterate over URLs and save each to a separate JSON file
for i, url in enumerate(urls, start=0):
    save_url_to_json(url, folder_path, i)
