


mockDict = {
    "https://www.youtube.com/watch?v=KOEfDvr4DcQ": "src/data/raw_videos/Face Your Biggest Fear To Win 800 000.mp4",
    "https://www.youtube.com/watch?v=krsBRQbOPQ4": "src/data/raw_videos/1 vs 250 000 000 Private Island!.mp4",
    "https://www.youtube.com/watch?v=7ESeQBeikKs": "src/data/raw_videos/Protect 500 000 Keep It!.mp4"
}


def fetch_video(url:str):
    return mockDict[url]

