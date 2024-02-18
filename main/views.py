from django.shortcuts import render

# Home page
def index(request):
    return render(request, 'index.html', {})

# About page
def about(request):
    return render(request, 'about.html', {})

# Contact page
def contact(request):
    return render(request, 'contact.html', {})

# Builder page
def builder(request):
    return render(request, 'builder.html', {})

# Builder page
def resume(request):
    return render(request, 'resume.html', {})
