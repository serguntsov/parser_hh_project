import psycopg2
from values import password_conn

conn = psycopg2.connect(
    host="localhost",
    database="hh",
    user="postgres",
    password= password_conn,
    port=5432
)

cursor = conn.cursor()

def get_vacancy_info(name, location, experience, salary_min, salary_max, value, id, id_user):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            name TEXT,
            location TEXT,
            experience TEXT,
            salary_min INTEGER NULL,
            salary_max INTEGER NULL,
            value TEXT,
            id TEXT,
            id_user BIGINT
        )
    """)

    salary_min = None if salary_min == "N/A" else salary_min
    
    salary_max = None if salary_max == "N/A" else salary_max
    
    salary_min = int(salary_min) if isinstance(salary_min, str) and salary_min.isdigit() else salary_min
    
    salary_max = int(salary_max) if isinstance(salary_max, str) and salary_max.isdigit() else salary_max
    
    try:
        cursor.execute("""
            INSERT INTO vacancies (name, location, experience, salary_min, salary_max, value, id, id_user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, location, experience, salary_min, salary_max, value, id, id_user))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
