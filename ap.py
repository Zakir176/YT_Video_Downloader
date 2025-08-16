#youtube playlistdownloader
#youtube playlistdownloader
import yt_dlp


url="https://youtu.be/OegyYwm6rqE?si=siaXLm_kdomMjw4R"

options={}

with yt_dlp.YoutubeDL(options) as yl:
    try:
        yl.download([url])
        print("✅ Playlist download completed.")


    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check the URL and try again.")