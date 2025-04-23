from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download')
def download():
    url = request.args.get('url')
    format_type = request.args.get('format')

    if not url or not format_type:
        return "URL ou formato ausente", 400

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    if format_type == 'mp4vtt':
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'writesubtitles': True,
            'subtitleslangs': ['pt'],
            'subtitlesformat': 'vtt',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        })
    elif format_type == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif format_type == 'vtt':
        ydl_opts.update({
            'skip_download': True,
            'writesubtitles': True,
            'subtitleslangs': ['pt'],
            'subtitlesformat': 'vtt',
        })
    else:
        return "Formato inválido", 400

    os.makedirs("downloads", exist_ok=True)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if format_type == 'mp3':
            filename = filename.rsplit('.', 1)[0] + '.mp3'
        elif format_type == 'vtt':
            filename = filename.rsplit('.', 1)[0] + '.pt.vtt'
        elif format_type == 'mp4vtt':
            filename = filename.rsplit('.', 1)[0] + '.mp4'

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
