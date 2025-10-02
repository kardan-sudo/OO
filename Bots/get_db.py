import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

conn_params = {
    "user": "postgres",
    "password": "2418908595",
    "host": "10.11.121.199",
    "port": "54320",
    "database": "sbp"
}
def get_event_list():
    event_list = []
    with psycopg2.connect(**conn_params) as connection:
        with connection.cursor() as cursor:
            cursor.execute("select event_type FROM public.events GROUP BY event_type;")
            records = cursor.fetchall()
            for record in records:
                event_list.append(record[0])

    return event_list


def get_event_data(event_type):
    with psycopg2.connect(**conn_params) as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(f"select id,title,event_type,start_date,end_date,address,description,website,phone FROM public.events where event_type = '{event_type}';")
            records = cursor.fetchall()

    return records

