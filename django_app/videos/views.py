from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from videos.models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import date
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

@login_required
def popular_videos(request):
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    current_month_videos = Video.objects.filter(
        created_at__month=current_month,
        created_at__year=current_year
    ).prefetch_related('likes', 'dislikes', 'comments')
    videos_with_popularity = []
    for video in current_month_videos:
        likes = video.likes.count()
        dislikes = video.dislikes.count()
        comments = video.comments.count()
        days_old = (today - video.created_at.date()).days      
        # Calcular popularidad
        #values
        ### likes = 10pts
        ### dislikes = -5pts
        ### comments = 1pt
        base_score = (likes * 10) - (dislikes * 5) + comments
        popularity = base_score * (1 - days_old)      
        videos_with_popularity.append({
            'video': video,
            'popularity': popularity
        })
    # Ordenar videos
    sorted_videos = sorted(videos_with_popularity, key=lambda x: -x['popularity'])   
    # Seleccionar top 5
    top_videos = [item['video'] for item in sorted_videos[:5]]
    # Manejar empates
    if len(top_videos) >= 5:
        first_popularity = sorted_videos[0]['popularity']
        if all(item['popularity'] == first_popularity for item in sorted_videos[:5]):
            top_videos = list(current_month_videos.order_by('?')[:5])
    
    paginator = Paginator(top_videos, 12)
    page = request.GET.get('page') 
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    return render(request, 'videos/popular.html', {'videos': videos})


#detail of videos
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    # Registrar visualización si el usuario está autenticado
    if request.user.is_authenticated:
        UserVideoHistory.objects.update_or_create(
            user=request.user,
            video=video,
            defaults={'viewed_at': timezone.now()}
        )
    #traer comentarios
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

#history of videos
@login_required
def view_history(request):
    history_list = UserVideoHistory.objects.filter(
        user=request.user
    ).select_related('video').order_by('-viewed_at')
    
    paginator = Paginator(history_list, 10)
    page = request.GET.get('page')
    try:
        history = paginator.page(page)
    except PageNotAnInteger:
        history = paginator.page(1)
    except EmptyPage:
        history = paginator.page(paginator.num_pages)   
    return render(request, 'videos/history.html', {'history': history})
