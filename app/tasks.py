from .celery import celery
from app import db
from app.models import Products

# Step#1 Deleting content of DB tables in PostgreSQL
@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, name='tasks.celery_task_del_table_content')
def celery_task_del_table_content(self):
    print("Just a test for celery_task_del_table_content - PASSED")
    return {'current': 100, 'total': 100, 'status': 'Очищення таблиць Products та Reviews в базі PostgreSQL відбулося успішно!', 'result': "Успішно!"}


# Step#2 Parsing data from Products.csv and Reviews.csv to PostgreSQL db
@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, name='tasks.celery_task_parse_csv_to_db')
def celery_task_parse_csv_to_db(self):
    print("Just a test for celery_task_parse_csv_to_db - PASSED")
    return {'current': 100, 'total': 100, 'status': 'Парсінг Products.csv та Reviews.csv в базу PostgreSQL відбувся успішно!', 'result': "Успішно!"}