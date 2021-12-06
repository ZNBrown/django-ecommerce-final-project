from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from django.urls import reverse

from .models import Community, Product
from .forms import CreateCommunityForm, AddProductForm
from members.forms import JoinCommunityForm
from members.models import Member

def my_communities(request):
    data = {
        'communities': Community.objects.all()
    }
    return render(request, "communities/my_communities.html", data)

def join_community(request):
    if request.method == 'POST':
        form = JoinCommunityForm(request.POST)
        if form.is_valid():
            form.save()
            comm_name = form.cleaned_data.get('comm_name')
            messages.success(request, f'Waiting for approval from {comm_name}')
            return redirect('my-communities')
    else:
        form = JoinCommunityForm()
    data = {'form': form}
    return render(request, 'communities/join_community.html', data)

def create_community(request):
    if request.method == 'POST':
        form = CreateCommunityForm(request.POST)
        if form.is_valid():
            form.save()
            comm_name = form.cleaned_data.get('comm_name')
            messages.success(request, f'Your new community, {comm_name}, has been created')
            return redirect('my-communities')
    else:
        form = CreateCommunityForm()
    data = {'form': form}
    return render(request, "communities/create_community.html", data)

def pending_requests(request):
    return render(request, "communities/pending_requests.html")

def community_page(request, community_id):
    data = {
        "community": Community.objects.filter(id=community_id)[0],
        "products": Product.objects.filter(community_id=community_id)
    }
    return render(request, "communities/community_page.html", data)

@login_required
def add_product(request, community_id):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            # product = form.save()
            form.user_id = request.user
            # form.user_id = 'katieched98@hotmail.co.uk'
            # form.community_id = 'Pathstow Village'
            form.save()
            print(request)
            product_title = form.cleaned_data.get('product_title')
            messages.success(request, f'Your product, {product_title}, has been added')
            return redirect(reverse('community-page', kwargs={"community_id": community_id}))    
    else:
        form = AddProductForm()
    data = {'form': form}
    return render(request, "products/add_product.html", data)

def basket_page(request):
    data = {
        "products": Product.objects.all(),
        "subtotal": Product.objects.aggregate(subtotal=Sum('price'))['subtotal'],
        "total": Product.objects.aggregate(total=Sum('price'))['total']
    }
    return render(request, "products/basket_page.html", data)

def product_page(request, community_id, product_id):
    data = {
        "community": Community.objects.filter(id=community_id)[0],
        "product": Product.objects.filter(id=product_id)[0]
    }
    return render(request, "products/product_page.html", data)

def not_found_404(request, exception):
    data = {'err': exception}
    return render(request, 'communities/404.html', data)

def server_error_500(request):
    return render(request, 'communities/500.html')

