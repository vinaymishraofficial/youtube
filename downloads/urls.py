from django.urls import path
from .views import download_video, download_playlist, get_video_details

urlpatterns = [
    path('', download_video, name='download_video'),
    path('playlist/', download_playlist, name='download_playlist'),
    path('get_video_details/', get_video_details, name='get_video_details'),
]
