from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from videos.models import Video
from .forms import VideoUploadForm
from django.shortcuts import get_object_or_404
#inicio de videos
def home(request):
    return render(request, 'home.html')
#cargar videos
@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect('video_detail', video_id=video.id)
    else:
        form = VideoUploadForm() 
    return render(request, 'videos/upload.html', {'form': form})
#dtealle de videos
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'videos/detail.html', {'video': video})
