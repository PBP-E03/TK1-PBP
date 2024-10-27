from django.urls import path
from .views import forum_index, post_create, post_detail, post_update, post_delete, upvote_post, downvote_post, post_comment, comment_edit, comment_delete
from . import views

app_name = 'forum_diskusi'

urlpatterns = [
    path('', forum_index, name='forum_index'),
    path('post/new/', post_create, name='post_create'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', post_update, name='post_update'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
    path('upvote/<int:post_id>/', upvote_post, name='post_upvote'),
    path('downvote/<int:post_id>/', downvote_post, name='post_downvote'),
    path('comment/<int:post_id>/', post_comment, name='post_comment'),
    path('comment/<int:pk>/edit/', comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', comment_delete, name='comment_delete'),
]