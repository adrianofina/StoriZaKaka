from django.contrib.auth.models import AbstractUser
from django.db import models
from djongo import models

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=30, blank=True, null=True)
    include_local_movies = models.BooleanField(default=False)
    theme = models.CharField(max_length=20, blank=True, null=True)
    content_rating = models.CharField(max_length=10, blank=True, null=True)

class Movie(models.Model):
    """
    Represents a movie.
    """
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    genres = models.JSONField(default=list)  # List of genre dicts or names
    rating = models.FloatField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=32, choices=[
        ('movie', 'Movie'),
        ('series', 'Series'),
        ('animation', 'Animation'),
        ('tvshow', 'TV Show'),
    ])
    country = models.CharField(max_length=64, blank=True)
    language = models.CharField(max_length=32, blank=True)
    poster_path = models.CharField(max_length=255, blank=True)
    backdrop_path = models.CharField(max_length=255, blank=True)
    release_date = models.CharField(max_length=32, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Genre(models.Model):
    """
    Represents a movie genre.
    """
    name = models.CharField(max_length=100)
    name_sw = models.CharField(max_length=100, blank=True, null=True)
    icon_name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10, blank=True, null=True)
    color_primary = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class UserWatchHistory(models.Model):
    """
    Tracks which user watched which movie and when.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)
    # Add other fields as needed

    def __str__(self):
        return f"{self.user.username} watched {self.movie.title}"

class RecommendationSession(models.Model):
    """
    Represents a recommendation session for a user.
    """
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add fields as needed, e.g. session data, results, etc.

    def __str__(self):
        return f"Session {self.id} for {self.user.username}"

class RecommendationResult(models.Model):
    """
    Stores the result of a recommendation session.
    """
    session = models.ForeignKey('RecommendationSession', on_delete=models.CASCADE, related_name='results')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    # Add other fields as needed

    def __str__(self):
        return f"{self.movie.title} (score: {self.score}) for session {self.session.id}"