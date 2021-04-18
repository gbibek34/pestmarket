from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html')),
    path('passsword-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html')),
    path('passsword-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html')),
    path('profile/', views.profile),
    path('checklogin/', views.homeredirect),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
