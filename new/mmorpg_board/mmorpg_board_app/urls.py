from django.urls import path
from .views import post_created, create_post, edit_post, post_detail, register, verification_sent, profile_view, \
    user_responses, delete_response, accept_response
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import subscribe_view

urlpatterns = [
    path('register/', register, name='register'),
    path('verification-sent/', verification_sent, name='verification_sent'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('', register, name='register_home'),
    path('post_created/', post_created, name='post_created'),
    path('create_post/', create_post, name='create_post'),
    path('accounts/profile/', profile_view, name='profile'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
    path('user_profile/', views.profile_view, name='user_profile'),
    path('user_responses/', user_responses, name='user_responses'),
    path('delete_response/<int:response_id>/', delete_response, name='delete_response'),
    path('accept_response/<int:response_id>/', accept_response, name='accept_response'),
    path('subscribe/', subscribe_view, name='subscribe'),
]
