from django.db import connection

def getTopRentedFilms(limit=5):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT f.title, c.name AS category, f.description, f.length, f.rating, f.special_features, f.release_year, COUNT(r.rental_id) AS rental_count
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