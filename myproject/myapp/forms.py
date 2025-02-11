from django import forms
from .models import Song, Author, Genre


class UploadSongForm(forms.ModelForm):
    username = forms.CharField(max_length=255, required=True, initial="")
    class Meta:
        model = Song
        fields = ['file', 'title', 'username']
