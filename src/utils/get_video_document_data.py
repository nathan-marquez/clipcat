import json
import os


def read_video_document(video_id):
    # Define the path to the video document based on the given video_id
    file_path = f"./data/video_documents/{video_id}.json"

    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file and load its content as a JSON object (dictionary)
        with open(file_path, "r") as file:
            video_document = json.load(file)
        return video_document
    else:
        # If the file does not exist, return an error message
        return {"error": "File does not exist"}


# Example usage
video_id = "12345"
video_document = read_video_document(video_id)
print(video_document)
