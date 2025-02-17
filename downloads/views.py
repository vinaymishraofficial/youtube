from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import YouTubeForm
import yt_dlp
import shutil

def fetch_video_details(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'force_generic_extractor': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        return info_dict

def get_video_details(request):
    url = request.GET.get('url')
    if url:
        try:
            video_details = fetch_video_details(url)
            thumbnail_url = video_details.get('thumbnail')
            return JsonResponse({'thumbnail_url': thumbnail_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'No URL provided'}, status=400)

def download_video(request):
    request.session['download_progress'] = '0%'
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            resolution = form.cleaned_data.get('resolution', '1080')
            print(f"Downloading video from URL: {url} at resolution: {resolution}")  # Debugging information
            try:
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        percent = d['_percent_str']
                        speed = d.get('_speed_str', 'N/A')
                        request.session['download_progress'] = percent
                        request.session['download_speed'] = speed
                    elif d['status'] == 'finished':
                        request.session['download_progress'] = '100%'
                        request.session['download_speed'] = '0'

                format_str = f'best[height<={resolution}]'

                ydl_opts = {
                    'format': format_str,
                    'progress_hooks': [progress_hook],
                    'outtmpl': '%(title)s.%(ext)s'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                return JsonResponse({'status': 'completed'})
            except Exception as e:
                print(f"Error downloading video: {e}")  # Debugging information
                return JsonResponse({'status': 'failed', 'error': str(e)})
    else:
        form = YouTubeForm()
    return render(request, 'downloads/index.html', {'form': form, 'progress': request.session.get('download_progress', '0%'), 'speed': request.session.get('download_speed', '0')})

def download_playlist(request):
    request.session['download_progress'] = '0%'
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            resolution = form.cleaned_data.get('resolution', '1080')
            print(f"Downloading playlist from URL: {url} at resolution: {resolution}")  # Debugging information
            try:
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        percent = d['_percent_str']
                        speed = d.get('_speed_str', 'N/A')
                        request.session['download_progress'] = percent
                        request.session['download_speed'] = speed
                    elif d['status'] == 'finished':
                        request.session['download_progress'] = '100%'
                        request.session['download_speed'] = '0'

                format_str = f'best[height<={resolution}]'

                ydl_opts = {
                    'format': format_str,
                    'progress_hooks': [progress_hook],
                    'outtmpl': '%(title)s.%(ext)s'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                return JsonResponse({'status': 'completed'})
            except Exception as e:
                print(f"Error downloading playlist: {e}")  # Debugging information
                return JsonResponse({'status': 'failed', 'error': str(e)})
    else:
        form = YouTubeForm()
    return render(request, 'downloads/playlist.html', {'form': form, 'progress': request.session.get('download_progress', '0%'), 'speed': request.session.get('download_speed', '0')})
