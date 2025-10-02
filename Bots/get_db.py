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
            cursor.execute(f"select id,title,event_type,start_date,end_date,address,description,website,phone,description_summ FROM public.events where event_type = '{event_type}';")
            records = cursor.fetchall()

    return records

def update_event_data_safe(event_id, **kwargs):
    """
    Безопасное обновление данных события с проверкой допустимых полей
    """
    allowed_fields = {
        'title', 'event_type', 'start_date', 'end_date', 
        'address', 'description', 'website', 'phone', 'description_summ'
    }
    
    update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not update_fields:
        return 0 
    
    with psycopg2.connect(**conn_params) as connection:
        with connection.cursor() as cursor:
            set_parts = []
            values = []
            
            for field, value in update_fields.items():
                set_parts.append(f"{field} = %s")
                values.append(value)
            
            values.append(event_id)
            
            sql = f"UPDATE public.events SET {', '.join(set_parts)} WHERE id = %s"
            cursor.execute(sql, values)
            connection.commit()
            
            return cursor.rowcount
        
update_event_data_safe(2, description_summ = 'test')