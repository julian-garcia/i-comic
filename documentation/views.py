from django.shortcuts import render

def view_documentation(request):
    return render(request, 'documentation.html')
