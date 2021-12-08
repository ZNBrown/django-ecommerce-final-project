from django.urls import path
from . import views
#note: not sure where to import this from
from communities.views import CreateCheckoutSessionView

urlpatterns = [
    # Index communities
    path('my-communities/', views.my_communities, name="my-communities"),
    # Show community / Index products
    path('my-communities/<int:community_id>/', views.community_page, name="community-page"),
    # New community
    path('my-communities/new/', views.create_community, name="create-community"),
    # Create membership
    path('join-community/', views.join_community, name="join-community"),
    # Index
    path('my-communities/<int:community_id>/pending-requests/', views.pending_requests, name="pending-requests"),
    # Show product
    path('my-communities/<int:community_id>/<int:product_id>/', views.product_page, name="product"),
    path('basket/', views.basket_page, name="basket"),
    # Create product
    path('my-communities/<int:community_id>/new/', views.add_product, name="add-product"),
    # Add paypal details in productpage
    path('paypal/details', views.recieve_seller_info, name="seller-info"),
]
