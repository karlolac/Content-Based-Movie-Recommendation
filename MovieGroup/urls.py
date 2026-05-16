from django.contrib import admin
from django.urls import path
# Uvozimo funkcije direktno iz tvoje aplikacije recommender_app:
from recommender_app.views import home, user_profile 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Početna stranica (Sustav preporuka)
    path('', home, name='home'), 
    
    # Nova stranica za korisnički profil
    path('profile/', user_profile, name='user_profile'),
]