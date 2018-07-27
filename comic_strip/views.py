from django.shortcuts import render

def comic_strip_listing(request):
    return render(request, 'comic_strips.html')
