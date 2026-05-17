from django.contrib import admin
from django.urls import path
from recommender_app.views import home, user_profile 
from django.contrib.auth import views as auth_views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), 
    path('profile/', user_profile, name='user_profile'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('<str:username>/', user_profile, name='user_profile_by_name'),
]