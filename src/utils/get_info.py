import requests
import re

api_key = "AIzaSyBPUWWsEu8CYp8DB1qDCwmyfGyU2MdmviM"  # Replace with your actual YouTube Data API v3 key


def get_info(video_url):

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
            thumbnail_url = video_data['snippet']['thumbnails']['high']['url']  # Assuming high quality thumbnail
            title = video_data['snippet']['title']
            views = video_data['statistics']['viewCount']
            likes = video_data['statistics'].get('likeCount', 'N/A')  # Likes might be disabled
            duration = video_data['contentDetails']['duration']
            description = video_data['snippet']['description']

            # Call parse_duration to convert duration to a more readable format
            readable_duration = parse_duration(duration)

            return {
                "url": video_url,
                "thumbnail_url": thumbnail_url,  # Add the thumbnail URL to the returned dictionary
                "title": title,
                "views": int(views),
                "likes": int(likes) if likes != 'N/A' else likes,
                "duration": readable_duration,
                "description": description,
            }
    else:
        return {"error": "Failed to fetch video information"}

def parse_duration(duration):
    # Match the duration parts
    pattern = re.compile(r'P(?:(\d+)D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(duration)
    days, hours, minutes, seconds = match.groups()

    # Convert the parts to integers, defaulting to 0 if not present
    days = int(days) if days else 0
    hours = int(hours) if hours else 0
    minutes = int(minutes) if minutes else 0
    seconds = int(seconds) if seconds else 0

    # Calculate total duration in seconds
    total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds

    # Format the duration
    if total_seconds < 3600:
        # Duration less than an hour, format as MM:SS
        return f'{minutes:02d}:{seconds:02d}'
    else:
        # Duration of an hour or more, include hours in the format
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

# Example usage
# video_url = "https://www.youtube.com/watch?v=KOEfDvr4DcQ"  # Replace with your video URL
# info = get_info(video_url)
# print(info)
