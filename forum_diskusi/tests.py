from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Vote
from resto.models import Restaurant
from django.utils import timezone

class ForumTestCase(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

        # Create and save a Restaurant object
        self.restaurant = Restaurant.objects.create(
            id=1,
            name="Test Restaurant",
            price=100,
            location="Test Location",
            special_menu="Test Menu",
            description="Test Description"
        )

        # Create and save a Post object
        self.post = Post.objects.create(
            id=1,
            title="Sample Post",
            content="This is a sample post for testing.",
            author=self.user,
            resto=self.restaurant
        )

        self.comment = Comment.objects.create(
            id=1,
            post=self.post,
            author=self.user,
            content="This is a test comment."
        )

    def test_forum_index(self):
        url = reverse('forum_diskusi:forum_index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum_diskusi/index.html')
        self.assertContains(response, self.post.title)

    def test_post_detail(self):
        url = reverse('forum_diskusi:post_detail', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum_diskusi/post_detail.html')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)

    def test_post_delete_author(self):
        url = reverse('forum_diskusi:post_delete', args=[self.post.id])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('forum_diskusi:forum_index'))
        # Check that the post has been deleted
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_post_update_author(self):
        url = reverse('forum_diskusi:post_update', args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum_diskusi/post_form.html')

        # Update the post
        response = self.client.post(url, {
            'title': 'Updated Title',
            'content': 'Updated content that is sufficiently long.',
            'resto': self.restaurant.id
        })
        self.assertRedirects(response, reverse('forum_diskusi:post_detail', args=[self.post.id]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_comment_edit_author(self):
        url = reverse('forum_diskusi:comment_edit', args=[self.comment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum_diskusi/comment_form.html')

        # Update the comment
        response = self.client.post(url, {
            'content': 'Updated comment content.'
        })
        self.assertRedirects(response, reverse('forum_diskusi:post_detail', args=[self.post.id]))
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment content.')

    def test_post_comment_valid(self):
        url = reverse('forum_diskusi:post_comment', args=[self.comment.id])
        response = self.client.post(url, {
            'content': 'This is a valid comment.'
        })
        self.assertRedirects(response, reverse('forum_diskusi:post_detail', args=[self.comment.id]))
        self.assertEqual(Comment.objects.count(), 2)

    def test_upvote_post(self):
        url = reverse('forum_diskusi:post_upvote', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.upvotes, 1)

    def test_downvote_post(self):
        url = reverse('forum_diskusi:post_downvote', args=[self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.downvotes, 1)
    
    def test_post_create_valid(self):
        url = reverse('forum_diskusi:post_create')
        # Get the list of available restaurants (assuming you use this in your form)
        available_restaurants = Restaurant.objects.all()
        # Use the first restaurant's ID for testing
        resto_id = available_restaurants[0].id

        response = self.client.post(url, {
            'title': 'New Post',
            'content': 'Content of the new post, which is definitely longer than 10 characters.',
            'resto': resto_id  # Include the 'resto' field
        })

        # Check redirect to forum index after creating a post
        self.assertRedirects(response, reverse('forum_diskusi:forum_index'))
        # Check that a new post has been created
        self.assertEqual(Post.objects.count(), 2)
        # Verify that the new post has the correct 'resto' associated
        new_post = Post.objects.get(title='New Post')
        self.assertEqual(new_post.resto.id, resto_id)
        self.assertEqual(new_post.author, self.user)
