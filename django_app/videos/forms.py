from django import forms
from .models import Video
import re
class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'embed_link']    
    def clean_embed_link(self):
        url = self.cleaned_data['embed_link']
        video_id = self.extract_video_id(url)      
        if not video_id:
            raise forms.ValidationError("URL de YouTube inválida")           
        return f'https://www.youtube.com/embed/{video_id}'  
    def extract_video_id(self, url):
        #validar que sea un link de youtube
        regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        match = re.search(regex, url)
        return match.group(1) if match else None