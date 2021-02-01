from django.db.models.query import ValuesListIterable
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile, Follow, Friend, FriendRequest, Rate
from post.models import Post, Like, Comment
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
import math, time

# Create your views here.

# Utils

def round_number(num):
    if num >= 1000 and num < 1000000:
        return f'{math.floor((num/1000)*10)/10}K'

    elif num >= 1000000:
        return f'{math.floor((num/1000000)*10)/10}M'

    else:
        return num


# Profile Page

def profile_page(request, username):
    # Requests
    if request.method == 'POST':
        # follow
        if request.POST.get('name', '') == 'follow':
            follower = request.POST.get('follower', '')
            following = request.POST.get('following', '')

            already_follow_check = Follow.objects.filter(follower=User.objects.filter(username=follower).first(), following=User.objects.filter(username=following).first()).count()

            if already_follow_check == 0:
                follow = Follow(follower=User.objects.filter(username=follower).first(), following=User.objects.filter(username=following).first())
                follow.save()

        # unfollow
        elif request.POST.get('name', '') == 'unfollow':
            follower = request.POST.get('follower', '')
            following = request.POST.get('following', '')
            Follow.objects.filter(follower=User.objects.filter(username=follower).first(), following=User.objects.filter(username=following).first()).delete()

        # like
        elif request.POST.get('name', '') == 'like':
            liker = User.objects.filter(username=request.POST.get('liker', '')).first()
            post = Post.objects.filter(pk=int(request.POST.get('post', ''))).first()

            already_like_check = Like.objects.filter(post=post, liker=liker).count()

            if already_like_check == 0:
                like = Like(post=post, liker=liker).save()

        # unlike
        elif request.POST.get('name', '') == 'unlike':
            liker = User.objects.filter(username=request.POST.get('liker', '')).first()
            post = Post.objects.filter(pk=int(request.POST.get('post', ''))).first()

            Like.objects.filter(post=post, liker=liker).delete()

        # Add comment
        elif request.POST.get('name', '') == 'add_comment':
            comment = request.POST.get('comment', '')
            commenter = User.objects.filter(username=request.POST.get('commenter', '')).first()
            post = Post.objects.filter(pk=int(request.POST.get('post', ''))).first()

            comment = Comment(post=post, commenter=commenter, comment=comment).save()

        # fetch comment
        elif request.POST.get('name', '') == 'comment_load':
            limit = 5
            offset = request.POST.get('offset', '')
            offset = int(offset)
            post_pk = request.POST.get('post', '')
            post = Post.objects.filter(pk=post_pk).first()

            comments = Comment.objects.filter(post=post)
            if comments.first() != None:
                comments = list(comments)[-offset:-(limit+offset):-1]
                comments_json = serializers.serialize('json', comments)

                u_d = []
                u__d = []
                c_time_passed = []
                for i in comments:
                    temp = Profile.objects.filter(user=i.commenter).first()
                    u_d.append(temp)
                    u__d.append(i.commenter)

                    # Calculating the time passed since the comment has been posted
                    # Split and get a list
                    dt = str(i.date).split('-')
                    # Taking 0th element because it is hour and we don't need mins and seconds
                    t = str(i.time).split(':')
                    # Now we have data like this - [Year, Month, Date, Hour]
                    dt.append(t[0])
                    dt.append(t[1])

                    # Now we have data corresponding to the current time - [Year, Month, Date, Hour]
                    r_dt = [time.strftime('%Y'), time.strftime('%m'), time.strftime('%d'), time.strftime('%H'), time.strftime('%M')]

                    if r_dt[0] == dt[0]: # year
                        tp = f'{int(r_dt[1]) - int(dt[1])} months ago'
                        if r_dt[1] == dt[1]: # month
                            tp = f'{int(r_dt[2]) - int(dt[2])} days ago'
                            if r_dt[2] == dt[2]: # date
                                tp = f'{int(r_dt[3]) - int(dt[3])} hours ago'
                                if r_dt[3] == dt[3]: # hour
                                    if (int(r_dt[4]) - int(dt[4])) == 0:
                                        tp = 'Few seconds ago'
                                    else:
                                        tp = f'{int(r_dt[4]) - int(dt[4])} minutes ago'

                        c_time_passed.append(tp)

                u_d_json = serializers.serialize('json', u_d)
                u__d_json = serializers.serialize('json', u__d)

                return JsonResponse(data={
                    'comments': comments_json,
                    'u_d': u_d_json,
                    'u__d': u__d_json,
                    'c_time_passed': c_time_passed,
                    'total': Comment.objects.filter(post=post).count(),
                })
            else:
                return JsonResponse(data={
                    'comments': None,
                    'u_d': None,
                    'u__d': None,
                    'c_time_passed': None,
                    'total': None,
                })

        # Rating
        elif request.POST.get('name', '') == 'rate':
            user = User.objects.filter(username=request.POST.get('user', '')).first()
            page = User.objects.filter(username=request.POST.get('page', '')).first()
            rating = request.POST.get('rating', '')

            Rate(user=user, page=page, rating=int(rating)).save()

    visit_user = get_object_or_404(User, username=username)

    # Variables to be sent
    visit = Profile.objects.filter(user=visit_user).first()
    try:
        auth = Profile.objects.filter(user=request.user).first()
    except:
        auth = None

    # Follow vars
    if auth != None:
        following = Follow.objects.filter(following=visit.user, follower=auth.user).count()
    else:
        following = None

    # Posts
    posts = Post.objects.filter(user=visit.user)
    num_of_total_likes = 0
    p = []
    if auth != None:
        for i in posts:
            l = Like.objects.filter(post=i, liker=auth.user).count()
            c = Like.objects.filter(post=i).count()
            co = Comment.objects.filter(post=i).count()
            p.append([i, l, c, co])
            num_of_total_likes += Like.objects.filter(post=i).count()
    elif auth == None:
        for i in posts:
            c = Like.objects.filter(post=i).count()
            co = Comment.objects.filter(post=i).count()
            p.append([i, 0, c, co])
            num_of_total_likes += Like.objects.filter(post=i).count()

    # stats
    num_of_followers = round_number(Follow.objects.filter(following=visit.user).count())
    num_of_following = round_number(Follow.objects.filter(follower=visit.user).count())

    # Rating
    if auth != None:
        rated = Rate.objects.filter(user=auth.user, page=visit.user).count()
    else:
        rated = None

    num_of_people_rated = 0
    page_rating = 0
    if Rate.objects.filter(page=visit.user).count() != 0:
        p_r_d = list(Rate.objects.filter(page=visit.user))
        for i in p_r_d:
            num_of_people_rated += 1
            page_rating += i.rating

        page_rating = int(page_rating/num_of_people_rated)

    params = {'visit': visit, 'auth': auth, 'following': following, 'num_of_followers': num_of_followers,
    'num_of_following': num_of_following, 'posts': p, 'num_of_total_likes': num_of_total_likes, 'rated': rated, 'num_of_people_rated': round_number(num_of_people_rated), 'page_rating': page_rating}

    return render(request, 'profile_page/index.html', params)

# Search
def search(request):
    q = request.POST.get('q', '')

    username = User.objects.filter(username__icontains=q)
    first_name = User.objects.filter(first_name__icontains=q)
    last_name = User.objects.filter(last_name__icontains=q)

    set_1 = set(username)
    set_2 = set(first_name)
    set_3 = set(last_name)

    dup = list(set_3 - set_2 - set_1)
    com = list(username) + dup

    c = serializers.serialize('json', com)

    u = []
    f = []
    l = []
    for i in username:
        u.append(Profile.objects.filter(user=i).first())
    for i in first_name:
        f.append(Profile.objects.filter(user=i).first())
    for i in last_name:
        l.append(Profile.objects.filter(user=i).first())

    set_1 = set(u)
    set_2 = set(f)
    set_3 = set(l)

    dup = list(set_3 - set_2 - set_1)
    com = u + dup

    r = serializers.serialize('json', com)


    return JsonResponse(data={
        'r': r,
        'c': c,
    })

# Account
@login_required(login_url='/log-in/')
def account(request):
    auth = Profile.objects.filter(user=request.user).first()

    params = {'auth': auth}
    return render(request, 'profile_page/account/index.html', params)

@login_required(login_url='/log-in/')
def account_profile(request):
    auth = Profile.objects.filter(user=request.user).first()

    params = {'auth': auth}
    return render(request, 'profile_page/account/profile.html', params)

def following(request, username):
    auth = Profile.objects.filter(user=request.user).first()
    visit = Profile.objects.filter(user=User.objects.filter(username=username).first()).first()

    # Following
    following = Follow.objects.filter(follower=auth.user)

    params = {'auth': auth, 'visit': visit, 'following': following}

    return render(request, 'profile_page/following.html', params)

def followers(request, username):
    pass