from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.view_history, name='view_history'),#historial de videos
    path('popular/', views.popular_videos, name='popular_videos'),#videos populares
    path('upload/', views.upload_video, name='upload_video'),#cargar videos
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),#detalle de videos
    path('video/<int:video_id>/like/', views.like_video, name='like_video'),#like de videos
    path('video/<int:video_id>/dislike/', views.dislike_video, name='dislike_video'),#no me gusta dislike
]