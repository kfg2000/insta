"""insta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from posts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('account/<int:author_id>', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('signup/', views.usersignup, name='signup'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),
    path('profile/', views.updateprofile, name='profile'),
    path('search/', views.search, name='search'),
    path('follow/<int:author_id>', views.follow, name='follow'),
    path('unfollow/<int:author_id>', views.unfollow, name='unfollow'),
    path('feed/', views.feed, name='feed'),
    path('ajax_like/<int:post_id>', views.ajax_like, name='ajax_like'),
    path('comment/<int:post_id>/<page>', views.comment, name='comment'),
    path('following/<int:author_id>', views.followinglist, name='following'),
    path('followers/<int:author_id>', views.followerslist, name='followers'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)