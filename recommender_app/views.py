import re
import requests
import urllib3
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserMovie
from recommendation_system import prepare_data, get_recommendations_from_list


metadata, cosine_sim, indices = prepare_data()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_poster_url(movie_title):
    clean = re.sub(r'\(.*?\)', '', movie_title).strip()
    
    if ',' in clean:
        parts = clean.split(',')
        last_part = parts[-1].strip().lower()
        if last_part in ['the', 'a', 'an']:
            clean = (parts[-1].strip() + " " + " ".join(parts[:-1]).strip()).strip()
    
    clean = clean.rstrip(',')

    api_key = "7717fa7262743faba2bd2f7714bb615d"
    base_url = "https://api.themoviedb.org/3/search/movie"
    
    params = {'api_key': api_key, 'query': clean}
    
    try:
        response = requests.get(base_url, params=params, verify=False, timeout=5)
        
        print(f"DEBUG: Status kod: {response.status_code} za film {clean}")
        
        if response.status_code != 200:
            print(f"⚠️ API Error: {response.text}")
            return "https://via.placeholder.com/500x750?text=API+Error"

        data = response.json()
        
        if data.get('results'):
            for result in data['results']:
                path = result.get('poster_path')
                if path:
                    poster_url = f"https://image.tmdb.org/t/p/w500{path}"
                    print(f"✅ USPJEH: {clean}")
                    return poster_url
        
        print(f"❌ TMDB nije našao rezultate za: {clean}")
        
    except Exception as e:
        print(f"⚠️ Sistemska greška: {e}")
    
    return "https://via.placeholder.com/500x750?text=No+Poster"

# @login_required <-- Ostavi zakomentirano dok ne napraviš login rute
def home(request):
    recommendations = None
    user_movies_display = None
    all_movie_titles = sorted(metadata['title'].unique().tolist())
    
  # Ako si prijavljen u /adminu, request.user će biti tvoj 'admin' račun
    if request.user.is_authenticated:
        current_user = request.user
    else:
        # Ako pristupaš stranici anonimno, umjesto kreiranja novog profila, 
        # sustav će jednostavno dohvatiti tvoj ručno kreirani 'admin' profil iz baze
        current_user = User.objects.filter(username='admin').first()
        
        # Ako iz nekog razloga nema admina, uzmi bilo kojeg prvog dostupnog korisnika
        if not current_user:
            current_user = User.objects.first()

    # 2. DOHVAĆANJE PODATAKA - Sada koristimo 'current_user' umjesto 'request.user'
    other_users = User.objects.exclude(id=current_user.id)
    my_movies = UserMovie.objects.filter(user=current_user).values_list('movie_title', flat=True)

    if request.method == 'POST':
        
        # SLUČAJ A: Dodavanje filma na profil
        if 'add_my_movie' in request.POST:
            selected_movie = request.POST.get('movie_title')
            if selected_movie in all_movie_titles:
                UserMovie.objects.get_or_create(user=current_user, movie_title=selected_movie)
            return redirect('home')

        # SLUČAJ B: Generiranje grupne preporuke
        elif 'generate_group' in request.POST:
            friend_id = request.POST.get('friend_id')
            
            combined_movie_list = list(my_movies)
            
            if friend_id:
                friend = User.objects.get(id=friend_id)
                friend_movies = UserMovie.objects.filter(user=friend).values_list('movie_title', flat=True)
                
                combined_movie_list.extend(list(friend_movies))
                user_movies_display = f"Moji filmovi + {friend.username}"
            else:
                user_movies_display = "Samo moji filmovi (Individualni prikaz)"

            combined_movie_list = list(set(combined_movie_list))
            
            if combined_movie_list:
                results = get_recommendations_from_list(combined_movie_list, metadata, cosine_sim, indices)
                
                if results is not None:
                    recommendations = results.to_dict('records')
                    for movie in recommendations:
                        movie['poster_url'] = get_poster_url(movie['title'])

    return render(request, 'recommender_app/home.html', {
        'recommendations': recommendations,
        'user_movies': user_movies_display,
        'all_movie_titles': all_movie_titles,
        'other_users': other_users,
        'my_movies': my_movies
    })

def user_profile(request):
    all_movie_titles = sorted(metadata['title'].unique().tolist())
    
    # Određivanje trenutnog korisnika (isto kao u home view-u)
    if request.user.is_authenticated:
        current_user = request.user
    else:
        current_user = User.objects.filter(username='admin').first() or User.objects.first()
        
    if not current_user:
        return redirect('home')
        
    # Ako korisnik želi obrisati film s profila
    if request.method == 'POST' and 'delete_movie' in request.POST:
        movie_to_delete = request.POST.get('movie_title')
        UserMovie.objects.filter(user=current_user, movie_title=movie_to_delete).delete()
        return redirect('user_profile')
        
    # Dohvati sve spremljene filmove za tog korisnika
    my_movies = UserMovie.objects.filter(user=current_user).order_by('-created_at')
    
    return render(request, 'recommender_app/profile.html', {
        'current_user': current_user,
        'my_movies': my_movies,
        'all_movie_titles': all_movie_titles
    })