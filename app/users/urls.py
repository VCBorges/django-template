from django.urls import path

from app.users import views

urlpatterns = [
    # templates
    path('login/', views.UserLoginTemplateView.as_view(), name='login_template'),
    path('signup/', views.UserCreateTemplateView.as_view(), name='signup_template'),
    path('profile/', views.UserProfileTemplateView.as_view(), name='profile_template'),
    # api
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('session/', views.UserLoginView.as_view(), name='login'),
    path('users/', views.UserCreateView.as_view(), name='create_list_users'),
    path('users/<uuid:pk>', views.UserUpdateView.as_view(), name='update_detail_users'),
]
