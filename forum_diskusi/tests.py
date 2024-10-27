from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Vote
from .forms import PostForm, CommentForm
from datetime import datetime
from django.utils import timezone

class ForumTests(TestCase):
    def setUp(self):
        # Membuat user untuk testing
        self.user = User.objects.create_user(username='user1', password='12345')
        self.client.login(username='user1', password='12345')
        
        # Membuat instance dari model Post untuk testing
        self.post = Post.objects.create(
            title='A valid title',
            content='This is a valid content with more than ten characters.',
            author=self.user,
            date_posted=timezone.now()
        )

    def test_post_comment_valid(self):
        # URL untuk post_comment view
        url = reverse('forum_diskusi:post_comment', kwargs={'post_id': self.post.id})
        response = self.client.post(url, {
            'content': 'This is a valid comment.'
        })
        
        # Memastikan bahwa redirect ke post_detail setelah comment valid
        self.assertRedirects(response, reverse('forum_diskusi:post_detail', kwargs={'pk': self.post.id}))

        # Memeriksa apakah comment berhasil disimpan
        self.assertEqual(self.post.comments.count(), 1)

    def test_upvote_post(self):
        url = reverse('forum_diskusi:upvote_post', kwargs={'post_id': self.post.id})
        response = self.client.post(url)

        # Mengambil post yang telah di-upvote
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.upvotes, 1)

    def test_downvote_post(self):
        url = reverse('forum_diskusi:downvote_post', kwargs={'post_id': self.post.id})
        response = self.client.post(url)

        # Mengambil post yang telah di-downvote
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.downvotes, 1)

    def test_post_create_valid(self):
        url = reverse('forum_diskusi:post_create')
        response = self.client.post(url, {
            'title': 'New valid title',
            'content': 'Content longer than 10 characters.'
        })

        # Memastikan bahwa redirect ke forum_index setelah membuat post
        self.assertRedirects(response, reverse('forum_diskusi:forum_index'))

        # Memeriksa apakah post berhasil disimpan
        self.assertEqual(Post.objects.count(), 2)

# Tambahkan lebih banyak test cases untuk memeriksa validasi, permissions, dan error handling.
