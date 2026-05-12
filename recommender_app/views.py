from django.shortcuts import render
from django.http import JsonResponse
# Importamo tvoj sustav koji si upravo sredio
from recommendation_system import prepare_data, get_recommendations_from_list

# Učitavamo podatke jednom pri pokretanju servera da bude brže
metadata, cosine_sim, indices = prepare_data()

def home(request):
    recommendations = None
    user_movies = None # Dodajemo ovo
    if request.method == 'POST':
        movie_input = request.POST.get('movies', '')
        user_movies = movie_input # Spremamo unos za prikaz
        movie_list = [m.strip() for m in movie_input.split(',')]
        
        results = get_recommendations_from_list(movie_list, metadata, cosine_sim, indices)
        
        if results is not None:
            recommendations = results.to_dict('records')

    # Dodaj user_movies u rječnik koji šalješ templateu
    return render(request, 'recommender_app/home.html', {
        'recommendations': recommendations,
        'user_movies': user_movies
    })