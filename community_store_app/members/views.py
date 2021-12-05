from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm

def signup(req):
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(req, f'Welcome, {first_name}!')
            return redirect('my-communities')
    else:
        form = SignUpForm()
    data = {'form': form}
    return render(req, 'members/signup.html', data)

# def joincommunity(req):
#     if req.method == 'POST':
#         form = JoinCommunityForm(req.POST)
#         if form.is_valid():
#             form.save()
#             comm_name = form.cleaned_data.get('comm_name')
#             messages.success(req, f'Waiting for approval from {comm_name}')
#             return redirect('my-communities')
#     else:
#         form = JoinCommunityForm()
#     data = {'form': form}
#     return render(req, 'communities/join_community.html', data)
