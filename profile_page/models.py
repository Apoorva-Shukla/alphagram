from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def getcurrentusername(instance, filename):
    '''uploading to the corresponding user's folder'''
    return f"{instance.user.username}/avatar/{filename}/"

# Profile related variables here
profile_settings_json = {"profile_photo": "everyone","profile_bio": "everyone","posts": "everyone","last_online": "nobody"}

class Profile(models.Model):
    '''
    Data of the user.

    user (ForeignKey) - Relation with the User Model
    avatar (ImageField) - Avatar of the user, for showing in profile page and comments
    '''

    '''profile data'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=getcurrentusername)

    '''Age data'''
    birth_year = models.IntegerField()
    birth_date = models.IntegerField()
    birth_month = models.CharField(max_length=20)

    '''social media'''
    instagram_handle = models.CharField(max_length=30, blank=True)
    twitter_handle = models.CharField(max_length=15, blank=True)

    '''other data'''
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=150, blank=True)
    date_joined = models.DateField(auto_now_add=True)
    time_joined = models.TimeField(auto_now_add=True)

    '''settings'''
    settings_profile_json = models.CharField(default=profile_settings_json, max_length=5000)

    '''method to filter database results'''
    def __str__(self):
        '''name of the user'''
        return self.user.username

class Follow(models.Model):
    '''
    Who is following whom
    '''

    '''Who is following'''
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    '''Who is being followed'''
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class FriendRequest(models.Model):
    '''
    Stores the friend request sent but not accepted.
    When a friend request is accepted it will be deleted from here and will be added to the Friends table.
    In other words this table stores the pending friend requets.

    r (Reciever) - The one whom the friend request has been sent to
    s (Sender) - The one who sent the friend request
    '''

    r = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_pending')
    s = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_pending')

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class Friend(models.Model):
    '''
    Friends table.

    r (Reciever) - The one who has accepted the friend request
    s (Sender) - The one who had sent the friend request
    '''

    r = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    s = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

class Rate(models.Model):
    '''
    Rate model, stores the rating of the users
    '''
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    page = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page')

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} rated {self.page.username} a {self.rating} star'