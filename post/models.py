from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def getcurrentusername(instance, filename):
    '''uploading to the corresponding user's folder'''
    return f"{instance.user.username}/post/{filename}/"


class Post(models.Model):
    '''
    Post model
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=getcurrentusername)
    caption = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} posted {self.caption}'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)