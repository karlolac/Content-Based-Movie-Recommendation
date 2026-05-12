import requests
from django.shortcuts import render
from recommendation_system import prepare_data, get_recommendations_from_list
import re
metadata, cosine_sim, indices = prepare_data()

def get_poster_url(movie_title):
    # 1. AGRESIVNO ČIŠĆENJE
    # Miče sve u zagradama: "Jumanji: Welcome to the Jungle (2017)" -> "Jumanji: Welcome to the Jungle"
    clean = re.sub(r'\(.*?\)', '', movie_title).strip()
    
    # 2. SREĐIVANJE ZAREZA (npr. "Incredibles, The" -> "The Incredibles")
    if ',' in clean:
        parts = clean.split(',')
        last_part = parts[-1].strip().lower()
        if last_part in ['the', 'a', 'an']:
            clean = (parts[-1].strip() + " " + " ".join(parts[:-1]).strip()).strip()
    
    # 3. DODATNO: Miče zareze koji su ostali na kraju
    clean = clean.rstrip(',')

    api_key = "7717fa7262743faba2bd2f7714bb615d"
    base_url = "https://api.themoviedb.org/3/search/movie"
    
    params = {'api_key': api_key, 'query': clean}
    
    try:
        response = requests.get(base_url, params=params, verify=False, timeout=5)
        
        # DEBUG: Ispisujemo status i sirovi odgovor
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

def home(request):
    recommendations = None
    user_movies_display = None
    all_movie_titles = sorted(metadata['title'].unique().tolist())

    if request.method == 'POST':
        movie_list_raw = request.POST.getlist('movie_titles[]')
        movie_list = [m.strip() for m in movie_list_raw if m.strip()]
        user_movies_display = ", ".join(movie_list)
        
        results = get_recommendations_from_list(movie_list, metadata, cosine_sim, indices)
        
        if results is not None:
            recommendations = results.to_dict('records')
            # KLJUČNI DIO: Dodajemo poster svakom filmu
            for movie in recommendations:
                movie['poster_url'] = get_poster_url(movie['title'])

    return render(request, 'recommender_app/home.html', {
        'recommendations': recommendations,
        'user_movies': user_movies_display,
        'all_movie_titles': all_movie_titles
    })