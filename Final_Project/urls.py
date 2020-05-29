"""Final_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from restaurant import views

urlpatterns = [
	path('admin/', admin.site.urls),
	path('restaurant/', views.home, name='home'),
	path('restaurant/<int:pid>/', views.home2, name='home2'),
	path('restaurant/login/', views.login, name='login'),
	path('restaurant/login/valid/', views.validation, name='validation'),
	path('restaurant/login/reg/', views.register, name='register'),
	path('restaurant/logout/', views.logout, name='logout'),
	path('restaurant/search/', views.search, name='search'),
	path('restaurant/search/<int:pid>/', views.search2, name='search2'),
	path('restaurant/detail/<str:business_id>', views.detail, name='detail'),
	path('restaurant/top/', views.top, name='top'),
	path('restaurant/userinfo/', views.userinf, name='userinfo'),
	path('restaurant/usrshow/<str:user_id>', views.usrshow, name='usrshow'),
	path('restaurant/map/', views.searchMap, name='map'),
	path('restaurant/analysis/', views.analysis, name='analysis'),
	path('restaurant/yelp_visualize', views.yelp_visualize, name='visualize')
]
