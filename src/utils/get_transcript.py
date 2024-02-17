from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_url):
    video_id = video_url.split('v=')[1]
    transcript = " ".join([entry['text'] for entry in YouTubeTranscriptApi.get_transcript(video_id)])

    return transcript

