import base64
import requests

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_caption(image_path):

    # Path to your image
    image_path = "src/data/video_scene_images/1/frame_1.png"

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

    return (response.json()["choices"][0]["message"]["content"])

# Example usage
if __name__ == "__main__":
    image_path = "src/data/video_scene_images/1/frame_1.png"  # Replace with the path to your image
    caption = get_image_caption(image_path)
    print(caption)