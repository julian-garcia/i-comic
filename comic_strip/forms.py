from django import forms
from .models import ComicStrip, ComicStripFrame

class ComicStripForm(forms.ModelForm):
    class Meta:
        model = ComicStrip
        fields = ['title', 'description']

class ComicStripFrameAddForm(forms.ModelForm):
    class Meta:
        model = ComicStripFrame
        fields = ['narrative', 'image']

class ComicStripFrameEditForm(forms.ModelForm):
    move = forms.IntegerField(required=False)
    class Meta:
        model = ComicStripFrame
        fields = ['narrative', 'image', 'move']
