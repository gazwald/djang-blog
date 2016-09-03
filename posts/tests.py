from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone

from .views import index, post_add, post_view
from .models import Post, Category
from .forms import PostForm


class TestPosts(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
                username="my_user",
                password="ALackOfSecurity",
                email="root@localhost.localdomain")

    def generic_post(self):
        return Post.objects.create( author=self.user,
                                    title='A Title',
                                    body='A Body',
                                    date_pub = timezone.now())

    def test_category_creation(self):
        new_cat = Category.objects.create(category='My Category')
        self.assertIsInstance(new_cat, Category)


    def test_post_creation(self):
        new_post = self.generic_post()
        self.assertIsInstance(new_post, Post)


    def test_view_post_index(self):
       request = self.factory.get('/posts/')
       response = index(request)
       self.assertEqual(response.status_code, 200)


    def test_view_post_id(self):
       new_post = self.generic_post()
       request = self.factory.get('/posts/1')
       response = post_view(request, 1)
       self.assertEqual(response.status_code, 200)


    def test_add_post(self):
        new_post = Post(
                    author=self.user,
                    title="Hello world",
                    body="I am a test post, isn't this great")
        self.assertEqual(new_post.title, "Hello world")


    def test_add_post_logged_in(self):
        request = self.factory.get('/posts/add/')
        request.user = self.user
        response = post_add(request)
        self.assertEqual(response.status_code, 200)


    def test_create_valid_post_logged_in(self):
        data = {'author': 1, 'title': 'Hello World', 'body': 'Another amazing post'}
        request = self.factory.post('/posts/add/', data)
        request.user = self.user
        response = post_add(request)
        self.assertEqual(response.status_code, 200)


    def test_add_post_anonymous(self):
        request = self.factory.get('/posts/add/', follow=True)
        request.user = AnonymousUser()
        response = post_add(request)
        self.assertEqual(response.status_code, 302)
