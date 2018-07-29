from django.shortcuts import render, redirect, reverse
from .forms import ComicStripForm, ComicStripFrameAddForm, ComicStripFrameEditForm
from .models import ComicStrip

def comic_strip_listing(request):
    comic_strips = ComicStrip.objects.all()
    return render(request, 'comic_strips.html', {'comic_strips': comic_strips})

def comic_strip(request):
    return render(request, 'comic_strip.html')

def comic_strip_add(request):
    if request.method=='POST':
        comic_strip_form = ComicStripForm(request.POST)
        if comic_strip_form.is_valid():
            comic_strip_form.save()
            return redirect(reverse('index'))
    else:
        comic_strip_form = ComicStripForm()

    return render(request, 'comic_strip_add.html',
                  {'comic_strip_form': comic_strip_form})
