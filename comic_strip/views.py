from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ComicStripForm, ComicStripFrameAddForm, ComicStripFrameEditForm
from .models import ComicStrip, ComicStripFrame

def index(request):
    '''
    Home page - product/process description
    '''
    return render(request, 'index.html')

def comic_strip_listing(request):
    '''
    Paginated listing of all comic strips defined by registered users. The
    pagination is in place to ensure that the page length does not affect
    usability due to excessive scrolling
    '''
    strips = ComicStrip.objects.all().order_by('title')

    paginator = Paginator(strips, 5)
    page = request.GET.get('page')
    comic_strips = paginator.get_page(page)

    return render(request, 'comic_strips.html', {'comic_strips': comic_strips})

def comic_strip(request, id):
    '''
    View the frames within a specific comic strip - effectively a self contained comic strip
    '''
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
    '''
    Registered users can add new comic strips. The login_required decorator
    will automatically redirect to the login page, as defined by LOGIN_URL in settings
    '''
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
    '''
    Within a comic strip, the author of that comic strip can add a new frame. A logged in
    user who is not the comic strip author will be denied this view with a suitable error
    message fed back to them.
    '''
    comic_strip = ComicStrip.objects.get(pk=id)

    if comic_strip.author == request.user:
        if request.method == 'POST':
            frame_form = ComicStripFrameAddForm(request.POST or None, request.FILES or None)

            if frame_form.is_valid():
                frame = frame_form.save(commit=False)
                # Auto increment the sequence number - used to display frames in the correct order
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
    else:
        messages.error(request, 'You must be the owner of this comic strip to add frames')
        return redirect(reverse('comic_strip', args=[comic_strip.id]))

    return render(request, 'frame_add.html', {'frame_form': frame_form, 'comic_strip': comic_strip})
