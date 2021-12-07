"""community_store_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from members import views as member_views
from communities import views as community_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('communities/', include('communities.urls')),
    path('signup/', member_views.signup, name='signup'),
    path('', auth_views.LoginView.as_view(template_name='members/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='members/login.html'), name='logout')
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

handler404 = 'communities.views.not_found_404'
handler405 = 'communities.views.method_not_allowed_405'
handler500 = 'communities.views.server_error_500'
