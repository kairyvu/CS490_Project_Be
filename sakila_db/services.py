from django.db import connection

def getAllFilms():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT f.film_id, f.title, f.description, f.release_year, f.rental_rate, f.length, f.rating, f.special_features, c.name AS category, COUNT(r.rental_id) AS rental_count
                       FROM film f
                       JOIN film_category fc ON f.film_id = fc.film_id
                       JOIN category c ON fc.category_id = c.category_id
                       JOIN inventory i ON f.film_id = i.film_id
                       LEFT JOIN rental r ON i.inventory_id = r.inventory_id
                       GROUP BY f.film_id, f.title, category
                       ORDER BY f.title;
                       """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

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
        cursor.execute(f"""SELECT f.title, f.description, f.release_year, f.rental_rate, f.length, f.rating, f.special_features, c.name AS category, COUNT(r.rental_id) AS rental_count
                       FROM film f
                       JOIN film_category fc ON f.film_id = fc.film_id
                       JOIN category c ON fc.category_id = c.category_id
                       JOIN inventory i ON f.film_id = i.film_id
                       LEFT JOIN rental r ON i.inventory_id = r.inventory_id 
                       WHERE f.film_id = {filmId}
                       GROUP BY f.film_id, c.name;
                       """)
        columns = [col[0] for col in cursor.description]
        result = cursor.fetchone()
        if result:
            return dict(zip(columns, result))
        return None
    
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
