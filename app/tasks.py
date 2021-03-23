from .celery import celery
from app import app, db
from app.models import Products, Reviews
import pandas as pd

# Step#1 Deleting content of DB tables in PostgreSQL
@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, name='tasks.celery_task_del_table_content')
def celery_task_del_table_content(self):
    db.session.commit()
    db.drop_all()
    db.create_all()
    db.session.close()
    print("celery_task_del_table_content - PASSED")
    return {'current': 100, 'total': 100, 'status': 'Очищення таблиць Products та Reviews в базі PostgreSQL відбулося успішно!', 'result': "Успішно!"}


# Step#2 Parsing data from Products.csv and Reviews.csv to PostgreSQL db
@celery.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, name='tasks.celery_task_parse_csv_to_db')
def celery_task_parse_csv_to_db(self):
    products_sheet_id = "1roypo_8amDEIYc-RFCQrb3WyubMErd3bxNCJroX-HVE"
    products_sheet_name = "Products"
    products_url_for_csv = f"https://docs.google.com/spreadsheets/d/{products_sheet_id}/gviz/tq?tqx=out:csv&sheet={products_sheet_name}"
    df_products = pd.read_csv(products_url_for_csv)
    print(df_products)
    # reordering columns:
    products_columns_reordered = ['Asin', 'Title']
    df_products_reordered = df_products[products_columns_reordered]
    print(df_products_reordered)
    # renaming columns:
    columns_for_df_products_reordered = df_products_reordered.columns.tolist()
    columns_for_df_products_reordered[0] = 'asin'
    columns_for_df_products_reordered[1] = 'title'
    df_products_reordered.columns = columns_for_df_products_reordered
    print(df_products_reordered)
    # saving to PostgreSQL:
    df_products_reordered.to_sql(name='products', con=db.engine, index=False, if_exists="append")

    reviews_sheet_id = "1iSR0bR0TO5C3CfNv-k1bxrKLD5SuYt_2HXhI2yq15Kg"
    reviews_sheet_name = "Reviews"
    reviews_url_for_csv = f"https://docs.google.com/spreadsheets/d/{reviews_sheet_id}/gviz/tq?tqx=out:csv&sheet={reviews_sheet_name}"
    df_reviews = pd.read_csv(reviews_url_for_csv)
    print("df_reviews", df_reviews)
    # renaming columns:
    columns_for_df_reviews_renamed = df_reviews.columns.tolist()
    print(columns_for_df_reviews_renamed)
    columns_for_df_reviews_renamed[0] = 'asin'
    columns_for_df_reviews_renamed[1] = 'title'
    columns_for_df_reviews_renamed[2] = 'review'
    df_reviews.columns = columns_for_df_reviews_renamed
    print(columns_for_df_reviews_renamed)
    #print(df_reviews)
    # saving to PostgreSQL:
    df_reviews.to_sql(name='reviews', con=db.engine, index=False, if_exists="append")

    print("Just a test for celery_task_parse_csv_to_db - PASSED")
    return {'current': 100, 'total': 100, 'status': 'Парсінг Products.csv та Reviews.csv в базу PostgreSQL відбувся успішно!', 'result': "Успішно!"}