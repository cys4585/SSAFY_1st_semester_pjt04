from django.shortcuts import render, redirect
from .models import Movie

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies':movies,
    }
    return render(request, 'movies/index.html', context)

def new(request):
    return render(request, 'movies/new.html')

def create(request):
    title = request.POST.get('title')
    overview = request.POST.get('overview')
    poster_path = request.POST.get('poster_path')
    # Movie.objects.create(title=title, overview=overview, poster_path=poster_path)
    # return redirect('movies:index')
    movie = Movie(title=title, overview=overview, poster_path=poster_path)
    movie.save()
    return redirect('movies:detail', movie.pk)


def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)

def delete(request, pk):
    if request.method == 'POST':
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return redirect('movies:index')
    else:
        return redirect('movies:detail', pk)

def edit(request, pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'movie':movie
    }
    return render(request, 'movies/edit.html', context)

def update(request, pk):
    if request.method == 'POST':
        title = request.POST.get('title')
        overview = request.POST.get('overview')
        poster_path = request.POST.get('poster_path')

        movie = Movie.objects.get(pk=pk)
        movie.title = title
        movie.overview = overview
        movie.poster_path = poster_path
        movie.save()
        return redirect('movies:detail', pk)
    return redirect('movies:edit', pk)