from django.shortcuts import render

from .models import Community, Product

# Create your views here.
def my_communities(request):
    return render(request, "communities/my_communities.html")

def join_community(request):
    return render(request, "communities/join_community.html")

def create_community(request):
    return render(request, "communities/create_community.html")

def pending_requests(request):
    return render(request, "communities/pending_requests.html")

def community_page(request, community_id):
    content = {
        "community": Community.objects.filter(id=community_id)[0],
        "products": Product.objects.filter(community_id=community_id)
    }
    return render(request, "communities/community_page.html", content)

def add_product(request):
    return render(request, "products/add_product.html")

def basket_page(request):
    return render(request, "products/basket_page.html")

def product_page(request):
    return render(request, "products/product_page.html")

