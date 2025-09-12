from django.urls import path
from . import views

urlpatterns = [
    path('account/register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('account/login/', views.UserLoginView.as_view(), name='user-login'),
    path('account/user/', views.UserView.as_view(), name='user-view'),
    path('account/logout/', views.UserLogoutView.as_view(), name='user-logout'),

]