import base64
import requests
import os

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_caption(image_path):

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "What’s in this image?"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response)
    print(response.json())

    return (response.json()["choices"][0]["message"]["content"])
   

def generate_captions_for_folder(folder_path):
    # Initialize a dictionary to store image paths and their captions
    captions_dict = {}

    # List all files in the given folder
    for image_file in os.listdir(folder_path):
        # Construct the full path to the image file
        image_path = os.path.join(folder_path, image_file)
        
        # Check if it's a file and not a subdirectory
        if os.path.isfile(image_path):
            # Use the existing function to get a caption for the image
            caption = get_image_caption(image_path)
            
            # Store the caption in the dictionary using the image file name as the key
            captions_dict[image_file[0]] = caption
    
    return captions_dict

# Example usage
if __name__ == "__main__":
    folder_path = "src/data/video_scene_images/1"  # Replace with your actual folder path
    captions_dict = generate_captions_for_folder(folder_path)
    
    # Print out the captions for each image
    for image_file, caption in captions_dict.items():
        print(f"{image_file}: {caption}")