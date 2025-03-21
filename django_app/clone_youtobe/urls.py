"""
URL configuration for clone_youtobe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from users import views as user_views
from django.contrib.auth.views import LogoutView
from videos.views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register_view, name='register'),
    path('login/', user_views.custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('', home, name='home'),#ruta inicial de videos
    path('videos/', include('videos.urls')),
]
