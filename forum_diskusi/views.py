import json
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from forum_diskusi.models import Post, Comment, Vote
from resto.models import Restaurant
from .forms import PostForm, CommentForm
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth.models import User 

logger = logging.getLogger(__name__)

@login_required
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            logger.info(f"Comment added by {request.user.username} on post '{post.title}'")
            return redirect('forum_diskusi:post_detail', pk=post.id)
        else:
            logger.error(f"Invalid comment form by {request.user.username}: {form.errors}")
    return redirect('forum_diskusi:post_detail', pk=post.id) 


@csrf_exempt
def upvote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    vote, created = Vote.objects.get_or_create(user=request.user, post=post)

    if request.method == 'POST':
        if not created and vote.vote_type == 'upvote':
            return JsonResponse({'error': 'You have already upvoted'}, status=400)
        elif not created and vote.vote_type == 'downvote':
            post.downvotes -= 1
            post.upvotes += 1
            vote.vote_type = 'upvote'
        else:
            post.upvotes += 1
            vote.vote_type = 'upvote'
        
        vote.save()
        post.save()
        return JsonResponse({'upvotes': post.upvotes, 'downvotes': post.downvotes})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def downvote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    vote, created = Vote.objects.get_or_create(user=request.user, post=post)

    if request.method == 'POST':
        if not created and vote.vote_type == 'downvote':
            return JsonResponse({'error': 'You have already downvoted'}, status=400)
        elif not created and vote.vote_type == 'upvote':
            post.upvotes -= 1
            post.downvotes += 1
            vote.vote_type = 'downvote'
        else:
            post.downvotes += 1
            vote.vote_type = 'downvote'
        
        vote.save()
        post.save()
        return JsonResponse({'upvotes': post.upvotes, 'downvotes': post.downvotes})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            logger.info(f"Post '{new_post.title}' created by {request.user.username}")
            return redirect('forum_diskusi:forum_index')
        else:
            logger.error(f"Invalid post form by {request.user.username}: {form.errors}")
    else:
        form = PostForm()
    return render(request, 'forum_diskusi/post_form.html', {'form': form, 'title': 'Create New Post'})

@csrf_exempt
def post_create_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_resto = get_object_or_404(Restaurant, name=data['restaurant'])
        new_title = data['title']
        new_content = data['content']
        new_post = Post(
            author = request.user,
            resto = new_resto,
            title = new_title,
            content = new_content
        )
        new_post.save()
        return JsonResponse({'status':'success'})
    return JsonResponse({'status': 'error'})

@csrf_exempt
def comment_create_flutter(request):
    if request.method == 'POST':
        try:
            # if not request.user.is_authenticated:
            #     return JsonResponse({
            #         'status': 'error',
            #         'message': 'User must be logged in to comment'
            #     }, status=401)

            data = json.loads(request.body)
            
            try:
                data_post = Post.objects.get(pk=data['post_id'])
            except Post.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f"Post with id {data['post_id']} does not exist"
                }, status=404)
            
            new_comment = Comment.objects.create(
                post=data_post,
                author=request.user,
                content=data['content']
            )
            
            return JsonResponse({
                'status': 'success',
                'comment': {
                    'id': new_comment.pk,
                    'content': new_comment.content,
                    'author': new_comment.author.username,
                    'date_posted': new_comment.date_posted.strftime("%Y-%m-%d %H:%M:%S")
                }
            })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

# forum_diskusi/views.py
def get_post_comments(request, pk):
    comments = Comment.objects.filter(post_id=pk)
    return HttpResponse(serializers.serialize('json', comments), content_type='application/json')

@csrf_exempt
@login_required
def get_user(request):
    return JsonResponse({
        'username': request.user.username,
        'status': 'success'
    })

def get_forum(request):
    data = Post.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_forum_by_id(request, id):
    data = Post.objects.filter(pk=id)
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

def get_username(request, id):
    data = get_object_or_404(User, pk=id)
    username = data.username
    return JsonResponse({'username':username})

def get_resto(request, id):
    data = get_object_or_404(Restaurant, pk=id)
    name = data.name
    return JsonResponse({'name':name})

def forum_index(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'forum_diskusi/index.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            logger.info(f"Comment added by {request.user.username} on post '{post.title}'")
            return redirect('forum_diskusi:post_detail', pk=post.pk)
        else:
            logger.error(f"Invalid comment form by {request.user.username}: {form.errors}")
    else:
        form = CommentForm()
    return render(request, 'forum_diskusi/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': form
    })


@csrf_exempt
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return JsonResponse({
            'status': 'error',
            'message': 'You are not authorized to edit this post'
        }, status=403)
    
    try:
        data = json.loads(request.body)
        post.title = data['title']
        post.content = data['content']
        post.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Post updated successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return JsonResponse({
            'status': 'error',
            'message': 'You are not authorized to delete this post'
        }, status=403)
    
    try:
        post.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Post deleted successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

# Jika menambahkan fitur edit/delete komentar
@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        logger.warning(f"{request.user.username} attempted to edit comment '{comment.id}' without permission")
        return redirect('forum_diskusi:post_detail', pk=comment.post.id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            logger.info(f"Comment '{comment.id}' edited by {request.user.username}")
            return redirect('forum_diskusi:post_detail', pk=comment.post.id)
        else:
            logger.error(f"Invalid comment edit form by {request.user.username}: {form.errors}")
    else:
        form = CommentForm(instance=comment)
    return render(request, 'forum_diskusi/comment_form.html', {'form': form})

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_id = comment.post.id
    if request.user == comment.author:
        comment.delete()
        logger.info(f"Comment '{pk}' deleted by {request.user.username}")
    else:
        logger.warning(f"{request.user.username} attempted to delete comment '{pk}' without permission")
    return redirect('forum_diskusi:post_detail', pk=post_id)

@csrf_exempt
def vote_forum(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            forum_id = data['forum_id']
            vote_type = data['vote_type']
            
            post = get_object_or_404(Post, pk=forum_id)
            
            if vote_type == 'upvote':
                if request.user in post.upvoted_by.all():
                    post.upvoted_by.remove(request.user)
                    post.upvotes -= 1
                else:
                    post.downvoted_by.remove(request.user)
                    post.upvoted_by.add(request.user)
                    post.upvotes += 1
                    if request.user in post.downvoted_by.all():
                        post.downvotes -= 1
            else:
                if request.user in post.downvoted_by.all():
                    post.downvoted_by.remove(request.user)
                    post.downvotes -= 1
                else:
                    post.upvoted_by.remove(request.user)
                    post.downvoted_by.add(request.user)
                    post.downvotes += 1
                    if request.user in post.upvoted_by.all():
                        post.upvotes -= 1
            
            post.save()
            return JsonResponse({
                'status': 'success',
                'upvotes': post.upvotes,
                'downvotes': post.downvotes
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)
