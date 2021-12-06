from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from .models import Community, Product

# Create your tests here.
class BaseTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
        cls.community = Community.objects.create(name='Laptop sellers', description ='desc Laptop sellers', location='location')
        cls.product = Product.objects.create(title='Laptop', description ='desc Laptop', price=10.99, sold_status=False, user_id=cls.user, community_id = cls.community)


class TestBasicViews(BaseTestCase):
    c = Client()

    def my_communities(self):
        response = self.c.get(reverse('my-communities'))
        assert "communities/my_communities.html" in [t.name for t in response.templates]
    
    def community_page(self):
        response = self.c.get(reverse('community-page'))
        assert "communities/community_page.html" in [t.name for t in response.templates]
    
    def create_community(self):
        response = self.c.get(reverse('create-community'))
        assert "communities/create-community.html" in [t.name for t in response.templates]

    def join_community(self):
        response = self.c.get(reverse('join_community'))
        assert "communities/join-community.html" in [t.name for t in response.templates]

    def pending_requests(self):
        response = self.c.get(reverse('community-page'))
        assert "communities/community_page.html" in [t.name for t in response.templates]
    

