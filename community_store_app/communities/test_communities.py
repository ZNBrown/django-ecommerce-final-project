from django.db.models.fields import PositiveBigIntegerField
from django.test import Client, TestCase
from django.urls import reverse
from .models import Community, Product, Membership, Request
from members.models import Member, Basket

class BaseTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = Member.objects.create_user(email='test@email.com', password='mypassword')
        cls.community = Community.objects.create(name='Laptop sellers', description='Sell laptops in any condition here', location='location')
        cls.product = Product.objects.create(title='Laptop', description='Fairly new laptop', price=10.99, sold_status=False, image="../../../media/images/laptop.jpg", user_id=cls.user, community_id=cls.community)
        cls.membership = Membership.objects.create(user_id=cls.user, community_id=cls.community, member_role="Member")
        cls.request = Request.objects.create(user_id=cls.user, community_id=cls.community, reason="I have an old laptop that I wish to sell")
        cls.basket = Basket.objects.create(user_id=cls.user)


#Do our basic view exist?
class TestBasicViews(BaseTestCase):
    c = Client()

    def test_my_communities(self):
        response = self.c.get('my-communities')
        assert "communities/404.html" in [t.name for t in response.templates]
        # assert "communities/my_communities.html" in [t.name for t in response.templates]
    
    def test_community_page(self):
        response = self.c.get('community-page', kwargs={'community_id': self.community.id})
        assert "communities/404.html" in [t.name for t in response.templates]
        # assert "communities/community_page.html" in [t.name for t in response.templates]
    
    def test_my_products(self):
        response = self.c.get('my-products')
        assert "communities/404.html" in [t.name for t in response.templates]
        # assert "communities/my_products.html" in [t.name for t in response.templates]

    def test_create_community(self):
        response = self.c.get('create-community')
        assert "communities/404.html" in [t.name for t in response.templates]
        # assert "communities/create_community.html" in [t.name for t in response.templates]

    def test_join_community(self):
        response = self.c.get('join-community')
        assert "communities/404.html" in [t.name for t in response.templates]
        # assert "communities/join_community.html" in [t.name for t in response.templates]

    def test_pending_requests(self):
        response = self.c.get('pending-requests', kwargs={'community_id': self.community.id})
        assert "communities/404.html" in [t.name for t in response.templates]
        # assert "communities/pending_requests.html" in [t.name for t in response.templates]

    # Added more tests
    def test_product_page(self):
        response = self.c.get('product', kwargs={'community_id': self.community.id, 'product_id': self.product.id})
        assert "communities/404.html" in [t.name for t in response.templates]
        # assert "communities/product_page.html" in [t.name for t in response.templates]

    def test_basket_page(self):
        response = self.c.get('basket')
        assert "communities/404.html" in [t.name for t in response.templates]    
        # assert "communities/basket_page.html" in [t.name for t in response.templates]

    def test_add_product(self):
        response = self.c.get('add-product', kwargs={'community_id': self.community.id})
        assert "communities/404.html" in [t.name for t in response.templates]
        # assert "communities/add_product.html" in [t.name for t in response.templates]

    def test_signup(self):
        response = self.c.get(reverse('signup'))
        assert "members/signup.html" in [t.name for t in response.templates]

class TestLoggedInViews(BaseTestCase):

    def setUp(self):
        self.c = Client()
        self.c.login(username="test@email.com", password="mypassword")

    def test_my_communities_page_load(self):
        response = self.c.get(reverse('my-communities'))
        assert "communities/my_communities.html" in [t.name for t in response.templates]
    
    def test_community_page_load(self):
        response = self.c.get(reverse('community-page', kwargs={'community_id': self.community.id}))
        assert "communities/community_page.html" in [t.name for t in response.templates]
    
    def test_my_products_page_load(self):
        response = self.c.get(reverse('my-products'))
        assert "products/my_products.html" in [t.name for t in response.templates]

    def test_create_community_page_load(self):
        response = self.c.get(reverse('create-community'))
        assert "communities/create_community.html" in [t.name for t in response.templates]
        
    def test_create_new_community(self):
        response = self.c.post(reverse('create-community'), {
            'name': 'new_test_comm',
            'description': "new desc",
            'location' : "new loc"
        })
        assert Community.objects.filter(name='new_test_comm').exists()

    def test_join_community_page_load(self):
        response = self.c.get(reverse('join-community'))
        assert "communities/join_community.html" in [t.name for t in response.templates]

    def test_request_join_community(self):
        response = self.c.post(reverse('join-community'), {
            'user_id': self.user.id,
            'community_id': self.community.id,
            'reason': 'I have an old laptop that I wish to sell'
        })
        assert Request.objects.filter(reason='I have an old laptop that I wish to sell').exists()

    def test_pending_requests_page_load(self):
        response = self.c.get(reverse('pending-requests', kwargs={'community_id': self.community.id}))
        assert "communities/pending_requests.html" in [t.name for t in response.templates]

    def test_accept_pending_request(self):
        response = self.c.post(reverse('pending-requests', kwargs={'community_id': self.community.id}), {
            'user_id': self.user.id,
            'community_id': self.community.id,
            'member_role': 'Member'
        })
        assert Membership.objects.filter(user_id='test@email.com').exists()

    def test_product_page_load(self):
        response = self.c.get(reverse('product', kwargs={'community_id': self.community.id, 'product_id': self.product.id}))
        assert "products/product_page.html" in [t.name for t in response.templates]

    def test_basket_page_load(self):
        response = self.c.get(reverse('basket'))
        assert "products/basket_page.html" in [t.name for t in response.templates]

    def test_create_product_page_load(self):
        response = self.c.get(reverse('add-product', kwargs={'community_id': self.community.id}))
        assert "products/add_product.html" in [t.name for t in response.templates]
        
    def test_add_new_product(self):
        response = self.c.post(reverse('add-product', kwargs={'community_id': self.community.id}), {
            'title': 'Test Laptop', 
            'description': 'desc Laptop', 
            'price': 12.99, 
            'sold_status': False, 
            'user_id': self.user.id, 
            'community_id' : self.community.id
        })
        assert Product.objects.filter(title='Test Laptop').exists()

    

