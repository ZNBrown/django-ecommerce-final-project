from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from django.urls import reverse
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views import View

url = settings.URL


from .models import Community, Product, Membership
from .forms import CreateCommunityForm, AddProductForm
from members.forms import JoinCommunityForm
from members.models import Member

def my_communities(request):
    data = {
        'communities': Community.objects.all(),
        'member': Membership.objects.all()
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

# This needs fixing
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


#sb-r9gkz8895206@personal.example.com
#DI/xD6cz
def basket_page(request):    
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
    }
    data = {
    'grant_type': 'client_credentials'
    }
    response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', headers=headers, data=data, 
    auth=('ATKw9NTm8MtV4AFn8bao8yyy_BvpBtMYpAXQQfG_gCe0q9RAbr8G605RyOxUorG9ozu5me2c2FAnblie', 'EEIRKOZ40ehETBuVQ2BQGsiKqmsDmTHNTVI8r9H5Fh86doKwXkpvABUdcxH4pXYPHEaMdx2EyV-O5cxM'))
    real_access_token = (response.json()['access_token'])
    # personal_client_id = "ATKw9NTm8MtV4AFn8bao8yyy_BvpBtMYpAXQQfG_gCe0q9RAbr8G605RyOxUorG9ozu5me2c2FAnblie"

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {real_access_token}',
    }
    data = '{\n    "tracking_id": "<Tracking-ID>",\n    "operations": [\n      {\n        "operation": "API_INTEGRATION",\n        "api_integration_preference": {\n          "rest_api_integration": {\n            "integration_method": "PAYPAL",\n            "integration_type": "THIRD_PARTY",\n            "third_party_details": {\n              "features": [\n                "PAYMENT",\n                "REFUND"\n             ]\n            }\n          }\n        }\n      }\n    ],\n    "products": [\n      "EXPRESS_CHECKOUT"\n    ],\n    "legal_consents": [\n      {\n        "type": "SHARE_DATA_CONSENT",\n        "granted": true\n      }\n    ]\n}'
    response = requests.post('https://api-m.sandbox.paypal.com/v2/customer/partner-referrals', headers=headers, data=data)
    action_url = response.json()['links'][1]['href']
    self_url = response.json()['links'][0]['href']
    print(action_url)





    data = {
        "products": Product.objects.all(),
        "subtotal": Product.objects.aggregate(subtotal=Sum('price'))['subtotal'],
        "total": Product.objects.aggregate(total=Sum('price'))['total'],
        "action_url" : action_url,
        "onboarding_tag" : f'<a data-paypal-button="true" href="{action_url}&displayMode=minibrowser" target="PPFrame">Sign up for PayPal</a>',
        "script_source": f'https://www.paypal.com/sdk/js?client-id=ATKw9NTm8MtV4AFn8bao8yyy_BvpBtMYpAXQQfG_gCe0q9RAbr8G605RyOxUorG9ozu5me2c2FAnblie&currency=GBP'
    }
    return render(request, "products/basket_page.html", data)

def product_page(request, community_id, product_id):
    data = {
        "community": Community.objects.filter(id=community_id)[0],
        "product": Product.objects.filter(id=product_id)[0]
    }
    return render(request, "products/product_page.html", data)

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
            success_url=(url + '/success/'),
            cancel_url=(url + '/cancel/'),
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

def server_error_500(request):
    return render(request, 'communities/500.html')
