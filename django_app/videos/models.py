from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
class Video(models.Model):
    title = models.CharField(max_length=200)
    embed_link = models.URLField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
