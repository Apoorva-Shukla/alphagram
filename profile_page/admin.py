from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(FriendRequest)
admin.site.register(Friend)
admin.site.register(Rate)