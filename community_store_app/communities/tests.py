from django.db.models.fields import PositiveBigIntegerField
from members.models import Member 
from django.test import Client, TestCase
from django.urls import reverse
from .models import Community, Product

# Create your tests here.
class BaseTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = Member.objects.create_user('myemail@crazymail.com', 'mypassword')
        cls.community = Community.objects.create(name='Laptop sellers', description ='desc Laptop sellers', location='location')
        cls.product = Product.objects.create(title='Laptop', description ='desc Laptop', price=10.99, sold_status=False, user_id=cls.user, community_id = cls.community)


#Do our basic view exist?
class TestBasicViews(BaseTestCase):
    c = Client()

    def test_my_communities(self):
        response = self.c.get(reverse('my-communities'))
        assert "communities/my_communities.html" in [t.name for t in response.templates]
    
    def test_community_page(self):
        response = self.c.get(reverse('community-page', kwargs={'community_id': self.community.id}))
        assert "communities/community_page.html" in [t.name for t in response.templates]
    
    def test_create_community(self):
        response = self.c.get(reverse('create-community'))
        assert "communities/create_community.html" in [t.name for t in response.templates]

    def test_join_community(self):
        response = self.c.get(reverse('join-community'))
        assert "communities/join_community.html" in [t.name for t in response.templates]

    # currently not working
    # def test_pending_requests(self):
    #     response = self.c.get(reverse('pending-requests', kwargs={'community_name': self.community.name}))
    #     assert "communities/pending_requests.html" in [t.name for t in response.templates]

class TestViewsRequiringData(BaseTestCase):

    def setUp(self):
        self.c = Client()
        self.c.login(username="myusername", password="mypassword")

    def test_create_new_community(self):
        response = self.c.post(reverse('create-community'), {
            'name': 'new_test_comm',
            'description': "new desc",
            'location' : "new loc"
        })
        assert Community.objects.filter(name='new_test_comm').exists()

    def test_create_new_product(self):
        response = self.c.post(reverse('add-product',  kwargs={'community_id': self.community.id}), {
            'title': 'Test Laptop', 
            'description': 'desc Laptop', 
            'price': 10.99, 
            'sold_status':False, 
            'user_id': self.user, 
            'community_id' : self.community
        })
        assert Product.objects.filter(title='Test Laptop').exists()

    # def test_show_page_load(self):
    #     response = self.c.get(reverse('dog-show', kwargs={'dog_id': self.dog.id}))
    #     assert "dogs/show.html" in [t.name for t in response.templates]

    

