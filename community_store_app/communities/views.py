from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Sum
from django.urls import reverse
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View

stripe.api_key = settings.STRIPE_SECRET_KEY
url = settings.URL


from .models import Community, Product, Membership, Request
from .forms import CreateCommunityForm, AddProductForm, AcceptRequest
from members.forms import JoinCommunityForm
from members.models import Member

@login_required
def my_communities(request):
    communities = Community.objects.filter(membership__user_id=request.user)
    for community in communities:
        community.member = Membership.objects.filter(user_id=request.user, community_id=community.id)[0]

    data = {
        'communities': communities
    }

    return render(request, "communities/my_communities.html", data)

@login_required
def join_community(request):
    if request.method == 'POST':
        form = JoinCommunityForm(request.POST)
        if form.is_valid():
            form.save()
            comm_name = form.cleaned_data.get('comm_name')
            messages.success(request, f'Waiting for approval from {comm_name}')
            return redirect('my-communities')
    else:
        form = JoinCommunityForm(initial={'user_id': request.user})
    data = {'form': form}
    return render(request, 'communities/join_community.html', data)

@login_required
def create_community(request):
    if request.method == 'POST':
        create_form = CreateCommunityForm(request.POST)
        # membership_form = AcceptRequest(request.POST)
        if create_form.is_valid():
            create_form.save()
            request.session["membership_form"] = request.POST.dict()
            comm_name = create_form.cleaned_data.get('comm_name')

            membership_form_data = request.session.pop('membership_form', {})
            community = membership_form_data.get("community_id")
            new_membership_form = AcceptRequest(initial={'user_id': request.user, 'community_id': community, 'member_role': "Admin"})
            if new_membership_form.is_valid():
                new_membership_form.save()
            # membership_form = AcceptRequest(community_id=comm_name)
            # if membership_form.is_valid():
            #     membership_form.save()
            messages.success(request, f'Your new community, {comm_name}, has been created')
            return redirect('my-communities')
    else:
        create_form = CreateCommunityForm()
        membership_form = AcceptRequest()
    data = {
        'create_form': create_form,
        'membership_form': membership_form
        }
    return render(request, "communities/create_community.html", data)

@login_required
def pending_requests(request, community_id):
    if request.method == "POST":
        if request.POST['type'] == 'POST':
            form = AcceptRequest(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'New member added to the community')
                Request.objects.filter(community_id=community_id, user_id=form.cleaned_data['user_id']).delete()

        elif request.POST['type'] == 'DELETE':
            form = AcceptRequest(request.POST)
            if form.is_valid():
                Request.objects.filter(community_id=community_id, user_id=form.cleaned_data['user_id']).delete()
            
        return redirect('pending-requests', community_id=community_id)

    join_requests = Request.objects.filter(community_id=community_id)
    for join_request in join_requests:
        join_request.form = AcceptRequest(initial={
            'user_id': join_request.user_id,
            'community_id': join_request.community_id,
            'member_role': 'Member',
            'request_id': join_request.id
        })
    data = {'join_requests': join_requests}
    return render(request, "communities/pending_requests.html", data)

@login_required
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
            form.save()
            product_title = form.cleaned_data.get('product_title')
            messages.success(request, f'Your product, {product_title}, has been added')
            messages.success(request, f'{request.user}')
            return redirect(reverse('community-page', kwargs={"community_id": community_id}))    
    else:
        form = AddProductForm(initial={'user_id': request.user, 'community_id': community_id})
    data = {'form': form}
    return render(request, "products/add_product.html", data)

@login_required
def basket_page(request):
    data = {
        "products": Product.objects.all(),
        "subtotal": Product.objects.aggregate(subtotal=Sum('price'))['subtotal'],
        "total": Product.objects.aggregate(total=Sum('price'))['total']
    }
    return render(request, "products/basket_page.html", data)

@login_required
def product_page(request, community_id, product_id):
    data = {
        "community": Community.objects.filter(id=community_id)[0],
        "product": Product.objects.filter(id=product_id)[0]
    }
    return render(request, "products/product_page.html", data)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

#note: dont know if i should be passing in Views 
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                #note: need to add data for our actual products in here
                {
                    'price_data': {
                        'currency': 'gbp',
                        'unit_amount': 40, #this is in pence
                        'product_data': {
                            'name': 'demo product one',
                            # 'images': ['image urls here'], #need to be publically available
                        }
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=("http://localhost:8000/communities/success/"),
            cancel_url=("http://localhost:8000/communities/cancel/"),
        )
        return JsonResponse({
            'id': checkout_session.id
        })

def success(request):
    return(request, "products/success.html", data)

def cancel(request):
    return(request, "products/cancel.html", data)

def not_found_404(request, exception):
    data = {'err': exception}
    return render(request, 'communities/404.html', data)

def method_not_allowed_405(request):
    return render(request, 'communities/405.html')
    
def server_error_500(request):
    return render(request, 'communities/500.html')
