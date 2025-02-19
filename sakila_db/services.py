from django.db import connection

def getTopRentedFilms(limit=5):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT f.film_id, f.title, c.name AS category, COUNT(r.rental_id) AS rental_count
                       FROM film f
                       JOIN film_category fc ON f.film_id = fc.film_id
                       JOIN category c ON fc.category_id = c.category_id
                       JOIN inventory i ON f.film_id = i.film_id
                       JOIN rental r ON i.inventory_id = r.inventory_id
                       GROUP BY f.film_id, f.title, category 
                       ORDER BY rental_count DESC, title
                       LIMIT {limit};
                       """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
def getFilmDetails(filmId):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT f.title, f.description, f.release_year, f.rental_rate, f.length, f.rating
                       FROM film f
                       WHERE f.film_id = {filmId};
                       """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
def getTopActors(limit=5):
    with connection.cursor() as cursor:
        cursor.execute(f"""
                       SELECT a.actor_id, a.first_name, a.last_name, COUNT(DISTINCT fa.film_id) AS movie_count
                       FROM actor a
                       JOIN film_actor fa ON a.actor_id = fa.actor_id
                       JOIN film f ON fa.film_id = f.film_id
                       JOIN inventory i ON f.film_id = i.film_id
                       GROUP BY a.actor_id, a.first_name, a.last_name
                       ORDER BY movie_count DESC
                       LIMIT {limit};
                       """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    

def getActorDetails(actorId):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT f.film_id, f.title, COUNT(r.rental_id) AS rental_count
                       FROM film f
                       JOIN film_actor fa ON f.film_id = fa.film_id
                       JOIN inventory i ON f.film_id = i.film_id
                       JOIN rental r ON i.inventory_id = r.inventory_id
                       WHERE fa.actor_id = {actorId}
                       GROUP BY f.film_id, f.title
                       ORDER BY rental_count DESC
                       LIMIT 5;
                       """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]