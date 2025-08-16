from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import yt_dlp
import subprocess
import shutil
import logging
from uuid import uuid4

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Configure download folder
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Check if FFmpeg is installed
def ffmpeg_installed():
    return shutil.which('ffmpeg') is not None

@app.route('/')
def index():
    return render_template('index.html', ffmpeg_available=ffmpeg_installed())

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    media_type = request.form.get('type')
    quality = request.form.get('quality')
    
    # Validate URL
    if not url or 'youtube.com/' not in url and 'youtu.be/' not in url:
        return {'status': 'error', 'message': 'Invalid YouTube URL'}, 400
    
    # Configure download options
    unique_id = str(uuid4())
    options = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{unique_id}.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
    }
    
    # Set format based on type and quality
    if media_type == 'audio':
        if ffmpeg_installed():
            options['format'] = 'bestaudio/best'
            options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            # Without FFmpeg, download best audio without conversion
            options['format'] = 'bestaudio'
    else:
        # Video formats that don't require merging
        if quality == 'high':
            options['format'] = 'best[height<=1080][ext=mp4]/best[ext=mp4]/best'
        elif quality == 'medium':
            options['format'] = 'best[height<=480][ext=mp4]/best[ext=mp4]'
        else:  # low
            options['format'] = 'worst[ext=mp4]/worst'
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Get the actual filename
            filename = ydl.prepare_filename(info)
            
            # For audio files with FFmpeg, change extension
            if media_type == 'audio' and ffmpeg_installed():
                filename = os.path.splitext(filename)[0] + '.mp3'
            
            # Send the file to the user
            return send_file(
                filename,
                as_attachment=True,
                download_name=os.path.basename(filename)
            )
    
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    # Warn about FFmpeg status
    if not ffmpeg_installed():
        print("WARNING: FFmpeg not found. Audio downloads will be in native format without conversion to MP3.")
    
    app.run(debug=True)