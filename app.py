from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import yt_dlp
from uuid import uuid4

app = Flask(__name__)

# Temporary storage for downloaded files
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    media_type = request.form.get('type')
    quality = request.form.get('quality')
    
    # Validate URL
    if not url or 'youtube.com/' not in url and 'youtu.be/' not in url:
        return redirect(url_for('index', error='Invalid YouTube URL'))
    
    # Configure download options
    options = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, f'{uuid4()}.%(ext)s'),
        'quiet': True,
    }
    
    # Set format based on type and quality
    if media_type == 'audio':
        options['format'] = 'bestaudio/best'
        options['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        if quality == 'high':
            options['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        elif quality == 'medium':
            options['format'] = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]'
        else:  # low
            options['format'] = 'worstvideo[ext=mp4]+worstaudio[ext=m4a]/worst[ext=mp4]'
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # For audio files, we need to change the extension
            if media_type == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'
            
            # Send the file to the user
            return send_file(filename, as_attachment=True)
    
    except Exception as e:
        return redirect(url_for('index', error=str(e)))

if __name__ == '__main__':
    app.run(debug=True)