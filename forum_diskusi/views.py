from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Vote
# from resto.models import Post
from .forms import PostForm, CommentForm
from django.urls import reverse
from django.http import JsonResponse
import logging

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

@login_required
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

@login_required
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

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        logger.warning(f"{request.user.username} attempted to edit post '{post.title}' without permission")
        return redirect('forum_diskusi:forum_index')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            logger.info(f"Post '{post.title}' updated by {request.user.username}")
            return redirect('forum_diskusi:post_detail', pk=post.pk)
        else:
            logger.error(f"Invalid post update form by {request.user.username}: {form.errors}")
    else:
        form = PostForm(instance=post)
    return render(request, 'forum_diskusi/post_form.html', {'form': form, 'title': 'Edit Post'})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        logger.warning(f"{request.user.username} attempted to delete post '{post.title}' without permission")
        return redirect('forum_diskusi:forum_index')
    post.delete()
    logger.info(f"Post '{post.title}' deleted by {request.user.username}")
    return redirect('forum_diskusi:forum_index')

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
