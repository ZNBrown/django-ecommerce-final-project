from django.urls import path
from . import views
#note: not sure where to import this from

urlpatterns = [
    path('my-communities/', views.my_communities, name="my-communities"),
    path('my-communities/<int:community_id>/', views.community_page, name="community-page"),
    path('my-products/', views.my_products, name="my-products"),
    path('my-communities/new/', views.create_community, name="create-community"),
    path('join-community/', views.join_community, name="join-community"),
    path('my-communities/<int:community_id>/pending-requests/', views.pending_requests, name="pending-requests"),
    path('my-communities/<int:community_id>/<int:product_id>/', views.product_page, name="product"),
    path('basket/', views.basket_page, name="basket"),
    path('my-communities/<int:community_id>/new/', views.add_product, name="add-product"),
    # Add paypal details in productpage
    path('paypal/details', views.recieve_seller_info, name="seller-info"),
    # attempt at cart
    path('cart/add', views.add_to_cart, name="add_to_cart"),
#     path('cart/remove', views.remove_from_cart, name="remove_from_cart"),
#     path('cart/view', views.get_cart, name="get_cart"),

]
