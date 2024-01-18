from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)


class UserProfile(models.Model):
    objects = None
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    verification_code = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Advertisement(models.Model):
    objects = None
    title = models.CharField(max_length=255)
    content = RichTextField()
    image1 = models.ImageField(upload_to='images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='images/', blank=True, null=True)
    video1 = models.URLField(blank=True, null=True)
    video2 = models.URLField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='advertisements')

    def __str__(self):
        return self.title


class Response(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_responses')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_responses',
                                 default=None)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Response from {self.sender.username} to {self.receiver.username}'


class Subscriber(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
