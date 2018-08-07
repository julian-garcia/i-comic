from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ComicStripForm, ComicStripFrameAddForm, ComicStripFrameEditForm
from .models import ComicStrip, ComicStripFrame

def comic_strip_listing(request):
    strips = ComicStrip.objects.all().order_by('title')

    paginator = Paginator(strips, 5)
    page = request.GET.get('page')
    comic_strips = paginator.get_page(page)

    return render(request, 'comic_strips.html', {'comic_strips': comic_strips})

def comic_strip(request, id):
    comic_strip = ComicStrip.objects.get(pk=id)
    description_words = len(comic_strip.description.split())
    frames = ComicStripFrame.objects.all().filter(comic_strip=comic_strip).order_by('sequence')

    paginator = Paginator(frames, 3)
    page = request.GET.get('page')
    comic_strip_frames = paginator.get_page(page)

    return render(request, 'comic_strip.html',
                  {'comic_strip': comic_strip,
                   'comic_strip_frames': comic_strip_frames,
                   'description_words': description_words})

@login_required
def comic_strip_add(request):
    if request.method=='POST':
        comic_strip_form = ComicStripForm(request.POST)

        if comic_strip_form.is_valid():
            comic_strip = comic_strip_form.save(commit=False)
            comic_strip.author = request.user
            comic_strip.save()
            return redirect(reverse('index'))
    else:
        comic_strip_form = ComicStripForm()

    return render(request, 'comic_strip_add.html',
                  {'comic_strip_form': comic_strip_form})

@login_required
def comic_strip_frame_add(request, id):
    comic_strip = ComicStrip.objects.get(pk=id)

    if request.method == 'POST':
        frame_form = ComicStripFrameAddForm(request.POST or None, request.FILES or None)

        if frame_form.is_valid():
            frame = frame_form.save(commit=False)
            frame.sequence = len(ComicStripFrame.objects.all().filter(comic_strip=comic_strip)) + 1
            frame.comic_strip = comic_strip
            frame.move = 0
            frame.save()
            return redirect(reverse('comic_strip', args=[comic_strip.id]))
        else:
            messages.error(request, 'Form filled in incorrectly')
            return redirect(reverse('comic_strip', args=[comic_strip.id]))
    else:
        frame_form = ComicStripFrameAddForm()

    return render(request, 'frame_add.html', {'frame_form': frame_form, 'comic_strip': comic_strip})
