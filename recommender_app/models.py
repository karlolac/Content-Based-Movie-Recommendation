from django.db import models
from django.contrib.auth.models import User

class UserMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_movies')
    # Maknut 'max_index=False', ostavljen samo ispravan 'db_index=True'
    movie_title = models.CharField(db_index=True, max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie_title')

    def __str__(self):
        return f"{self.user.username} - {self.movie_title}"