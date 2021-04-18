from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html')),
    path('profile/', views.profile),
    path('password/', views.password),
    path('checklogin/', views.homeredirect),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
