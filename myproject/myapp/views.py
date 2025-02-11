from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db import models
from .forms import UploadSongForm
from .models import Song, Author, Genre
import os
from django.conf import settings

def upload_and_list_files(request):
    if request.method == 'POST':
        form = UploadSongForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            username = form.cleaned_data['username']
            file = form.cleaned_data['file']

            authors_data = request.POST.getlist('authors[]')
            genres_data = request.POST.getlist('genres[]')

            song = Song.objects.create(title=title, username=username, file=file)
            
            authors = [Author.objects.get_or_create(name=author)[0] for author in authors_data if author]
            genres = [Genre.objects.get_or_create(name=genre)[0] for genre in genres_data if genre]
            
            song.authors.set(authors)
            song.genres.set(genres)

            return redirect('upload_and_list_files')
    else:
        form = UploadSongForm()

    # Delete non-existing files from database
    for song in Song.objects.all():
        file_path = os.path.join(settings.MEDIA_ROOT, str(song.file))
        if not os.path.exists(file_path):
            song.delete()

    # Search by criteria
    query = request.GET.get('q', '')
    songs = Song.objects.filter(
        models.Q(title__icontains=query) |
        models.Q(authors__name__icontains=query) |
        models.Q(genres__name__icontains=query) |
        models.Q(username__icontains=query)
    ).distinct()

    # Pagination
    per_page = request.GET.get('per_page', 5)
    try:
        per_page = int(per_page) if per_page else 5
    except ValueError:
        per_page = 5

    paginator = Paginator(songs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'upload_and_list.html', {'form': form, 'page_obj': page_obj, 'query': query})
