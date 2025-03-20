from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from videos.models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#home videos
def home(request):
    videos = Video.objects.annotate(
        total_comments=Count('comments'),
        total_likes=Count('likes')
    ).order_by('?') 
    
    paginator = Paginator(videos, 12)
    page = request.GET.get('page')
    
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'videos': videos})
#upload videos 
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
#detail of videos

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comments = video.comments.all()  
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = video
            comment.save()
            return redirect('video_detail', video_id=video_id)
    else:
        form = CommentForm()
    return render(request, 'videos/detail.html', {
        'video': video,
        'comments': comments,
        'user': request.user  ,
        'form': CommentForm()
    })
#like de videos
@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user = request.user
    
    if video.user_has_disliked(user):
        video.dislikes.remove(user)
    
    if video.user_has_liked(user):
        video.likes.remove(user)
    else:
        video.likes.add(user)
    
    return redirect('video_detail', video_id=video_id)
#dislike
@login_required
def dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user = request.user
    
    if video.user_has_liked(user):
        video.likes.remove(user)
    
    if video.user_has_disliked(user):
        video.dislikes.remove(user)
    else:
        video.dislikes.add(user)
    
    return redirect('video_detail', video_id=video_id)
