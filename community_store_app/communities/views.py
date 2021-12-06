from django.shortcuts import render
from django.db.models import Sum

from .models import Community, Product
from members.forms import JoinCommunityForm

def my_communities(request):
    return render(request, "communities/my_communities.html")

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
    return render(request, "communities/create_community.html")

def pending_requests(request):
    return render(request, "communities/pending_requests.html")

def community_page(request, community_id):
    data = {
        "community": Community.objects.filter(id=community_id)[0],
        "products": Product.objects.filter(community_id=community_id)
    }
    return render(request, "communities/community_page.html", data)

def add_product(request):
    return render(request, "products/add_product.html")

def basket_page(request):

    data = {
        "products": Product.objects.all(),
        "subtotal": Product.objects.aggregate(subtotal=Sum('price'))['subtotal'],
        "total": Product.objects.aggregate(total=Sum('price'))['total']
    }
    return render(request, "products/basket_page.html", data)

def product_page(request):
    return render(request, "products/product_page.html")

def not_found_404(request, exception):
    data = {'err': exception}
    return render(request, 'communities/404.html', data)

def server_error_500(request):
    return render(request, 'communities/500.html')

