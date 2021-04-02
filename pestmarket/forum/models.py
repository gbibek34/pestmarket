from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_time = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='nothing.jpg', upload_to='posted_pics')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-view', kwargs={'pk': self.pk})


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='liked_post')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='liking_user')
    liked = models.BooleanField(default=False)

    def is_liked(self):
        self.liked = True
        self.save()

    def not_liked(self):
        self.liked = False
        self.save()
