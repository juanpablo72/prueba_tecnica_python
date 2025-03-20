from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
##commetarios
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f"Comentario de {self.user.username} en {self.video.title}"
#model for videos of youtube
class Video(models.Model):
    title = models.CharField(max_length=200)
    embed_link = models.URLField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='video_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='video_dislikes', blank=True)
    def __str__(self):
        return self.title
    def total_likes(self):
        return self.likes.count()
    def total_dislikes(self):
        return self.dislikes.count()
    def user_has_disliked(self, user):
        return self.dislikes.filter(id=user.id).exists()
    def user_has_liked(self, user):
        return self.likes.filter(id=user.id).exists() if user.is_authenticated else False
#model for user video history
class UserVideoHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-viewed_at']
        verbose_name_plural = 'Historial de usuarios'
    def __str__(self):
        return f"{self.user.username} vio {self.video.title} en {self.viewed_at}"