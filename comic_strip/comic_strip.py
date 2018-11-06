from .forms import ComicStripForm, ComicStripFrameAddForm
from .models import ComicStripFrame

def commit_strip(request):
    commit_strip.comic_strip_form = ComicStripForm(request.POST)

    if commit_strip.comic_strip_form.is_valid():
        comic_strip = commit_strip.comic_strip_form.save(commit=False)
        comic_strip.author = request.user
        comic_strip.save()
    
def commit_frame(request, comic_strip):
    commit_frame.frame_form = ComicStripFrameAddForm(request.POST or None, request.FILES or None)

    if commit_frame.frame_form.is_valid():
        frame = commit_frame.frame_form.save(commit=False)
        # Auto increment the sequence number - used to display frames in the correct order
        frame.sequence = len(ComicStripFrame.objects.all().filter(comic_strip=comic_strip)) + 1
        frame.comic_strip = comic_strip
        frame.move = 0
        frame.save()