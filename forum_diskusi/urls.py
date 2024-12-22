from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import forum_index, get_forum_by_id,get_post_comments, get_resto,  get_user, get_forum, get_username, post_create, comment_create_flutter, post_create_flutter, post_detail, post_update, post_delete, upvote_post, downvote_post, post_comment, comment_edit, comment_delete, vote_forum
from . import views

app_name = 'forum_diskusi'

urlpatterns = [
    path('', forum_index, name='forum_index'),
    path('get-username/<int:id>', get_username, name='get_username'),
    path('get-resto/<int:id>', get_resto, name='get_resto'),
    path('post/new/', post_create, name='post_create'),
    path('post/get-all/', get_forum, name='get_forum'),
    path('post/get-<int:id>/', get_forum_by_id, name='get_forum_by_id'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', post_update, name='post_update'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
    path('upvote/<int:post_id>/', upvote_post, name='post_upvote'),
    path('downvote/<int:post_id>/', downvote_post, name='post_downvote'),
    path('comment/<int:post_id>/', post_comment, name='post_comment'),
    path('comment/<int:pk>/edit/', comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', comment_delete, name='comment_delete'),
    path('post/new-flutter/', post_create_flutter, name='post_create_flutter'),
    path('post/new-comment/', comment_create_flutter, name='comment_create_flutter'),
    path('get-user/', get_user, name='get_user'),
    path('post/<int:pk>/comments/', get_post_comments, name='get_post_comments'),
    path('vote-forum/', vote_forum, name='vote_forum'),
]