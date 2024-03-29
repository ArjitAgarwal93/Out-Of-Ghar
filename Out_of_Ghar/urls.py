"""
URL configuration for Out_of_Ghar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from .views import homepage,blog_approval
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    #Home page
    path('',homepage,name='home'),
    path('approve/',blog_approval,name='approve_page'),

    #accounts
    path('account/',include('accounts.urls')),

    #blog
    path('blog/',include('blog.urls')),

    #userProfile
    path('userProfile/',include('userProfile.urls')),

    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

