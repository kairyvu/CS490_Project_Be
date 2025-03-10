from django.db import transaction, connection
from .models import Customer, Address, City, Country
from django.db import transaction
from django.db.utils import IntegrityError

def getAllFilms():
    with connection.cursor() as cursor:
        cursor.execute("""SELECT f.film_id, f.title, f.description, f.release_year, f.rental_rate, f.length, f.rating, f.special_features, c.name AS category, COUNT(r.rental_id) AS rental_count, GROUP_CONCAT(DISTINCT CONCAT(UCASE(LEFT(a.first_name, 1)), LCASE(SUBSTRING(a.first_name, 2)), ' ', UCASE(LEFT(a.last_name, 1)), LCASE(SUBSTRING(a.last_name, 2))) ORDER BY a.first_name SEPARATOR ', ') AS actors
                       FROM film f
                       JOIN film_category fc ON f.film_id = fc.film_id
                       JOIN category c ON fc.category_id = c.category_id
                       JOIN inventory i ON f.film_id = i.film_id
                       LEFT JOIN rental r ON i.inventory_id = r.inventory_id
                       JOIN film_actor fa ON f.film_id = fa.film_id
                       JOIN actor a ON fa.actor_id = a.actor_id
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
        cursor.execute(f"""SELECT f.title, f.description, f.release_year, f.rental_rate, f.length, f.rating, f.special_features, c.name AS category, COUNT(r.rental_id) AS rental_count, GROUP_CONCAT(DISTINCT CONCAT(UCASE(LEFT(a.first_name, 1)), LCASE(SUBSTRING(a.first_name, 2)), ' ', UCASE(LEFT(a.last_name, 1)), LCASE(SUBSTRING(a.last_name, 2))) ORDER BY a.first_name SEPARATOR ', ') AS actors 
                       FROM film f
                       JOIN film_category fc ON f.film_id = fc.film_id
                       JOIN category c ON fc.category_id = c.category_id
                       JOIN inventory i ON f.film_id = i.film_id
                       LEFT JOIN rental r ON i.inventory_id = r.inventory_id
                       LEFT JOIN film_actor fa ON f.film_id = fa.film_id
                       LEFT JOIN actor a ON fa.actor_id = a.actor_id
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


def getAllCustomers():
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT customer.customer_id, customer.first_name, customer.last_name, customer.email, customer.active, address.address, address.district, city.city, country.country, address.phone, customer.create_date
                       FROM customer
                       JOIN address ON customer.address_id = address.address_id
                       JOIN city ON address.city_id = city.city_id
                       JOIN country ON city.country_id = country.country_id
                       ORDER BY customer.customer_id;
                       """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
def getCustomerRentalHistory(customerId):
    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT c.first_name, c.last_name, f.title AS film_title, r.rental_date, r.return_date,
                       CASE 
                        WHEN r.return_date IS NULL THEN 'Currently Rented'
                        ELSE 'Returned'
                       END AS rental_status
                       FROM customer c
                       JOIN address a ON c.address_id = a.address_id
                       JOIN rental r ON c.customer_id = r.customer_id
                       JOIN inventory i ON r.inventory_id = i.inventory_id
                       JOIN film f ON i.film_id = f.film_id
                       WHERE c.customer_id = {customerId}
                       ORDER BY r.rental_date DESC;
                       """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def update_customer_info(customer_data):
    try:
        with transaction.atomic():
            customer = Customer.objects.get(customer_id=customer_data['customer_id'])
            customer.first_name = customer_data['first_name']
            customer.last_name = customer_data['last_name']
            customer.email = customer_data['email']
            customer.save()

            address = customer.address
            address.address = customer_data['address']
            address.district = customer_data['district']
            address.phone = customer_data['phone']
            address.save()

            city = address.city
            city.city = customer_data['city']
            city.save()

            country = city.country
            country.country = customer_data['country']
            country.save()

        return {"message": "Customer and related records updated successfully"}

    except Customer.DoesNotExist:
        return {"error": "Customer not found"}
    except Address.DoesNotExist:
        return {"error": "Address not found for the customer"}
    except City.DoesNotExist:
        return {"error": "City not found for the address"}
    except Country.DoesNotExist:
        return {"error": "Country not found for the city"}
    except Exception as e:
        return {"error": str(e)}

def execute_sql_query(query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

def get_next_id(table_name):
    query = f"SELECT MAX({table_name}_id) FROM {table_name};"
    result = execute_sql_query(query)
    return result[0][0] + 1 if result[0][0] is not None else 1

def create_customer_info(customer_data):
    try:
        with transaction.atomic():
            country_name = customer_data['country']
            query = "SELECT country_id FROM country WHERE country = %s;"
            country_result = execute_sql_query(query, [country_name])

            if country_result:
                country_id = country_result[0][0]
            else:
                country_id = get_next_id('country') 
                query = "INSERT INTO country (country_id, country) VALUES (%s, %s);"
                execute_sql_query(query, [country_id, country_name])

            city_name = customer_data['city']
            query = "SELECT city_id FROM city WHERE city = %s AND country_id = %s;"
            city_result = execute_sql_query(query, [city_name, country_id])

            if city_result:
                city_id = city_result[0][0]
            else:
                city_id = get_next_id('city')
                query = "INSERT INTO city (city_id, city, country_id) VALUES (%s, %s, %s);"
                execute_sql_query(query, [city_id, city_name, country_id])

            address_data = customer_data['address']
            district = customer_data['district']
            phone = customer_data['phone']
            query = """
                SELECT address_id FROM address WHERE address = %s AND district = %s AND phone = %s AND city_id = %s;
            """
            address_result = execute_sql_query(query, [address_data, district, phone, city_id])

            if address_result:
                address_id = address_result[0][0]
            else:
                address_id = get_next_id('address')
                query = """
                    INSERT INTO address (address_id, address, district, phone, city_id) 
                    VALUES (%s, %s, %s, %s, %s);
                """
                execute_sql_query(query, [address_id, address_data, district, phone, city_id])

            first_name = customer_data['first_name']
            last_name = customer_data['last_name']
            email = customer_data['email']

            print(f"c_id: {last_name}")

            query = """
                INSERT INTO customer (first_name, last_name, email, address_id, create_date, store_id)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP(), 1);
            """
            execute_sql_query(query, [first_name, last_name, email, address_id])
            return {"message": "Customer and related records added successfully"}

    except IntegrityError as e:
        return {"error": "Integrity error - possibly duplicate key", "detail": str(e)}
    except Exception as e:
        return {"error": "An error occurred while adding the customer", "detail": str(e)}