from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Sum
from django.urls import reverse
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponse, response
from django.views import View

url = settings.URL

from .models import Community, Product, Membership, Request
from .forms import CreateCommunityForm, AddProductForm, AcceptRequest
from members.forms import JoinCommunityForm
from members.models import Member, Basket
import json

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
        if create_form.is_valid():
            new_community = create_form.save()
            post_data = request.POST.copy()
            post_data.update({'community_id': new_community.id})
            membership_form = AcceptRequest(post_data)
            if membership_form.is_valid():
                membership_form.save()

                messages.success(request, f'Your new community, {new_community.name}, has been created')
                return redirect('my-communities')
            else:
                print(membership_form.errors)
    else:
        create_form = CreateCommunityForm()
        membership_form = AcceptRequest(initial={'user_id': request.user, 'member_role': 'Admin'})
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

def recieve_seller_info(request):
    format_req = json.loads(request.body.decode("utf-8"))
    print(format_req)

    authcode = format_req["authCode"]
    sharedId = format_req["sharedId"]
    nonce = format_req["sellerNonce"]
    user = Member.objects.filter(id=format_req["userId"])[0]
    user.authcode = authcode
    user.sharedId = sharedId
    user.save()
    response = HttpResponse("DONT COME HERE")
    return response

@login_required
def my_products(request):
    #PARTNER/OUR MARKET REQUEST TO GET OUR ACCESS TOKEN
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
    }
    data = {
    'grant_type': 'client_credentials'
    }
    response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', headers=headers, data=data, 
    #our client secret stuff (dont peek!)
    auth=('ATKw9NTm8MtV4AFn8bao8yyy_BvpBtMYpAXQQfG_gCe0q9RAbr8G605RyOxUorG9ozu5me2c2FAnblie', 'EEIRKOZ40ehETBuVQ2BQGsiKqmsDmTHNTVI8r9H5Fh86doKwXkpvABUdcxH4pXYPHEaMdx2EyV-O5cxM'))
    real_access_token = (response.json()['access_token'])
    seller_nonce = request.user.seller_nonce

    #Onboarding stuff for selllers: need a business account to recieve funds
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {real_access_token}',
    }

    data =  '{ "partner_config_override": { "return_url": "http://localhost:8000/communities/basket/"}, "operations": [      {        "operation": "API_INTEGRATION",        "api_integration_preference": {          "rest_api_integration": {            "integration_method": "PAYPAL",            "integration_type": "FIRST_PARTY",            "first_party_details": {              "features": [                "PAYMENT",                "REFUND"              ],              "seller_nonce": "%s"            }          }        }      }    ],    "products": [      "EXPRESS_CHECKOUT"    ],    "legal_consents": [      {        "type": "SHARE_DATA_CONSENT",        "granted": true      }    ]}'%(seller_nonce)

    response = requests.post('https://api-m.sandbox.paypal.com/v2/customer/partner-referrals', headers=headers, data=data)
    print("----------------")
    action_url = response.json()['links'][1]['href']
    self_url = response.json()['links'][0]['href']
    print(self_url)
    requests.get(self_url)
    products = Product.objects.filter(user_id=request.user)
    for product in products:
        product.community = Community.objects.filter(name=product.community_id)[0]

    data = {
        "products": products,
        "action_url" : action_url,
        "seller_nonce" : seller_nonce,
        "user" : request.user.id
    }
    return render(request, "products/my_products.html", data)


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
        data = {'form': form, 
                "user" : request.user.id
                }
    return render(request, "products/add_product.html", data)


#sb-r9gkz8895206@personal.example.com
#DI/xD6cz
@login_required
def basket_page(request):
    basket = Basket.objects.filter(user_id=request.user)[0]
    print(basket) 
    basket2 = Product.objects.filter(baskets = basket)[0]
    basket3 = Product.objects.filter(baskets = basket)
    print(basket2)    
    #---------------------------------------------------------
    #REQUEST 3: assemble access token    
    data = {
    'grant_type': 'authorization_code',
    'code': basket2.user_id.authcode,
    'code_verifier': basket2.user_id.seller_nonce
    }
    print(basket2.user_id.sharedId)
    response = requests.post('https://api-m.sandbox.paypal.com/v1/oauth2/token', data=data, auth=(basket2.user_id.sharedId, ''))
    print("----------")
    print(response)
    print(response.json())
    print("----------")
    try:
        if (response.json()['error']):
            access_token = "dummy"
    except:
        print(response.json())
        access_token = response.json()["access_token"]

    headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    }

    response = requests.get('https://api-m.sandbox.paypal.com/v1/customer/partners/HK3JGUX62WFZ8/merchant-integrations/credentials/', headers=headers)

    try: 
        if (response.json()['error']):
            client_id = "dummy"
    except:
        print(response.json())
        client_id = response.json()["client_id"]



    merchant_id = request.GET.get('merchantIdInPayPal')
    print(merchant_id)




    data = {
        "products": basket3,
        "subtotal": basket3.aggregate(subtotal=Sum('price'))['subtotal'],
        "total": basket3.aggregate(total=Sum('price'))['total'],
        "client_id": client_id, 
        "merchant_id_in_paypal": merchant_id,
        "script_source": f'https://www.paypal.com/sdk/js?client-id=ATKw9NTm8MtV4AFn8bao8yyy_BvpBtMYpAXQQfG_gCe0q9RAbr8G605RyOxUorG9ozu5me2c2FAnblie&currency=GBP'
    }
    print("-0-0-0-0-0-0-0-0-0-0-0--0-0-0-0-")
    print(data)
    return render(request, "products/basket_page.html", data)

@login_required
def product_page(request, community_id, product_id):
    data = {
        "community": Community.objects.filter(id=community_id)[0],
        "product": Product.objects.filter(id=product_id)[0],
        'user_id': request.user.id,
        'product_id': Product.objects.filter(id=product_id)[0].id

    }
    return render(request, "products/product_page.html", data)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def not_found_404(request, exception):
    data = {'err': exception}
    return render(request, 'communities/404.html', data)

def method_not_allowed_405(request):
    return render(request, 'communities/405.html')
    
def server_error_500(request):
    return render(request, 'communities/500.html')


def add_to_cart(request):
    format_req = json.loads(request.body.decode("utf-8"))
    print(format_req)
    product = Product.objects.get(id=format_req["product_id"])
    user = Member.objects.get(id=format_req["user_id"])
    print('000000')
    print(Basket.objects.filter(user_id=user)[0])
    product.baskets.add(Basket.objects.filter(user_id=user)[0])
    product.save()
    print(product.baskets.all())
    response = HttpResponse("Backend route. Shoo!")
    return response

# def remove_from_cart(request, product_id):
#     product = Product.objects.get(id=product_id)
#     cart = Cart(request)
#     cart.remove(product)

# def get_cart(request):
#     response = HttpResponse("Backend route. Shoo!")
#     return response

