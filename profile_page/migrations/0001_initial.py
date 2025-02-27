# Generated by Django 3.1.4 on 2021-01-11 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import profile_page.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to=profile_page.models.getcurrentusername)),
                ('birth_year', models.IntegerField()),
                ('birth_date', models.IntegerField()),
                ('birth_month', models.CharField(max_length=20)),
                ('instagram_handle', models.CharField(blank=True, max_length=30)),
                ('twitter_handle', models.CharField(blank=True, max_length=15)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('bio', models.TextField(blank=True, max_length=150)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('time_joined', models.TimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('r', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_pending', to='profile_page.profile')),
                ('s', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_pending', to='profile_page.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('r', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='profile_page.profile')),
                ('s', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='profile_page.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='profile_page.profile')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='profile_page.profile')),
            ],
        ),
    ]
