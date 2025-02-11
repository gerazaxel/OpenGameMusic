from django.db import models
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    file = models.FileField(upload_to='uploads/')
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default='Anonymous') # Replaced ForeignKey with CharField
    authors = models.ManyToManyField(Author, through='SongAuthor')
    genres = models.ManyToManyField(Genre, through='SongGenre')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} by {', '.join([author.name for author in self.authors.all()])} ({', '.join([genre.name for genre in self.genres.all()])})"


class SongGenre(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('song', 'genre')


class SongAuthor(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('song', 'author')
