import requests

def get_info(api_key, video_url):
    # Extract the video ID from the URL
    video_id = video_url.split('v=')[1]
    api_url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet,contentDetails,statistics'

    # Make the API request
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            video_data = data['items'][0]
            # Extract the required information
            title = video_data['snippet']['title']
            views = video_data['statistics']['viewCount']
            likes = video_data['statistics'].get('likeCount', 'N/A')  # Likes might be disabled
            duration = video_data['contentDetails']['duration']
            description = video_data['snippet']['description']

            # Placeholder for transcript. You would need to integrate a method to fetch this.
            transcript = "Transcript not available through the API."

            # Formatting duration to a more readable format if necessary could be added here

            return {
                "url": video_url,
                "title": title,
                "views": int(views),
                "likes": int(likes) if likes != 'N/A' else likes,
                "duration": duration,  # Consider converting ISO 8601 duration to a readable format
                "description": description,
                "transcript": transcript,
            }
    else:
        return {"error": "Failed to fetch video information"}

# Example usage
api_key = "AIzaSyBPUWWsEu8CYp8DB1qDCwmyfGyU2MdmviM"  # Replace with your actual YouTube Data API v3 key
video_url = "https://www.youtube.com/watch?v=KOEfDvr4DcQ"  # Replace with your video URL
info = get_info(api_key, video_url)
print(info)
