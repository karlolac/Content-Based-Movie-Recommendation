# Content-Based Movie Recommendation System and Application for User Groups

Ovaj projekt predstavlja web aplikaciju razvijenu u sklopu završnog rada, koja kombinira **Content-Based sustav preporuka filmova** s naprednom logikom za **generiranje zajedničkih preporuka za grupe korisnika**. Sustav analizira pojedinačne profile i povijest gledanja odabranih članova grupe te pronalazi optimalne filmske preporuke koje zadovoljavaju zajedničke interese svih odabranih korisnika.

## 🚀 Ključne Funkcionalnosti
* **Osobni profil:** Svaki korisnik ima svoj profil na koji može dodavati filmove koje je pogledao ili mu se sviđaju.
* **Brzo upravljanje:** Dodavanje filmova odvija se putem tražilice s automatskim dovršavanjem (Autocomplete), dok se brisanje neželjenih filmova može odraditi jednim klikom izravno s početne stranice.
* **Grupna preporuka (Killer Feature):** Mogućnost označavanja (checkbox) više različitih korisnika odjednom. Sustav u pozadini agregira njihove podatke i računa preporuku za cijelu ekipu.
* **Vizualni prikaz (TMDB API):** Aplikacija dinamički povlači stvarne plakate filmova i pripadajuće žanrove u stvarnom vremenu.

## 🛠️ Tehnološki Stog (Tech Stack)
* **Backend:** Python 3, Django Web Framework
* **Data Science & Algoritmi:** Pandas, Scikit-learn (TF-IDF Vectorizer, Cosine Similarity)
* **Frontend:** HTML5, Bootstrap 5 (Responsive UI), Bootstrap Icons
* **Vanjski API:** The Movie Database (TMDB) API za dohvaćanje plakata

---

## 💻 Kako pokrenuti projekt lokalno?

###  Kloniranje repozitorija
```bash
git clone [https://github.com/karlolac/Content-Based-Movie-Recommendation.git](https://github.com/karlolac/Content-Based-Movie-Recommendation.git)
cd Content-Based-Movie-Recommendation

pip install -r requirements.txt

python manage.py runserver  (http://127.0.0.1:8000/)
