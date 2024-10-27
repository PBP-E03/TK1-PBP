from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from resto.models import Restaurant


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    resto = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.title

    def clean(self):
        if len(self.content) < 10:
            raise ValidationError('Content is too short.')

class Vote(models.Model):
    VOTE_TYPES = (
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)

    class Meta:
        unique_together = ('user', 'post')  # Menghindari voting ganda

    def __str__(self):
        return f'{self.user.username} {self.vote_type} {self.post.title}'

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'

    def clean(self):
        if len(self.content) < 5:
            raise ValidationError('Comment is too short.')
