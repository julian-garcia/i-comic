from django import forms
from .models import ComicStrip, ComicStripFrame

class ComicStripForm(forms.ModelForm):
    class Meta:
        model = ComicStrip
        fields = ['title', 'description']

class ComicStripFrameAddForm(forms.ModelForm):
    class Meta:
        model = ComicStripFrame
        fields = ['comic_strip', 'narrative', 'image']

class ComicStripFrameEditForm(forms.ModelForm):
    class Meta:
        model = ComicStripFrame
        fields = ['comic_strip', 'narrative', 'image', 'move']
