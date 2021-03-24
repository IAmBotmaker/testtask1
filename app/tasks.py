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
    return {'current': 100, 'total': 100, 'status': 'Очищення таблиць Products та Reviews в базі PostgreSQL відбулося '
                                                    'успішно!', 'result': "Успішно!"}


# Step#2 Parsing data from Products.csv and Reviews.csv to PostgreSQL db
@celery.task(bind=True, name='tasks.celery_task_parse_csv_to_db')  # autoretry_for=(Exception,), retry_backoff=True
def celery_task_parse_csv_to_db(self):
    # Parsing Products.csv to dataframe
    products_sheet_id = "1roypo_8amDEIYc-RFCQrb3WyubMErd3bxNCJroX-HVE"
    products_sheet_name = "Products"
    products_url_for_csv = f"https://docs.google.com/spreadsheets/d/{products_sheet_id}/gviz/tq?tqx=out:csv&sheet=" \
                           f"{products_sheet_name}"
    df_products = pd.read_csv(products_url_for_csv)
    df_products['id'] = df_products.index  # converting id from index of df to column ['id']
    # reordering columns:
    products_columns = ['Asin', 'Title', 'id']
    df_products_updated = df_products[products_columns]
    # renaming columns:
    columns_for_df_products_updated = df_products_updated.columns.tolist()
    columns_for_df_products_updated[0] = 'asin'
    columns_for_df_products_updated[1] = 'title'
    columns_for_df_products_updated[2] = 'id'
    df_products_updated.columns = columns_for_df_products_updated

    # Parsing Reviews.csv to dataframe
    reviews_sheet_id = "1iSR0bR0TO5C3CfNv-k1bxrKLD5SuYt_2HXhI2yq15Kg"
    reviews_sheet_name = "Reviews"
    reviews_url_for_csv = f"https://docs.google.com/spreadsheets/d/{reviews_sheet_id}/gviz/tq?tqx=out:csv&sheet=" \
                          f"{reviews_sheet_name}"
    df_reviews = pd.read_csv(reviews_url_for_csv)
    # renaming columns:
    columns_for_df_reviews = df_reviews.columns.tolist()
    columns_for_df_reviews[0] = 'asin'
    columns_for_df_reviews[1] = 'title'
    columns_for_df_reviews[2] = 'review'
    df_reviews.columns = columns_for_df_reviews
    # mapping product_ids from df_products_updated and saving it to dataframe column
    df_reviews['product_ids'] = df_reviews['asin'].map(df_products_updated.set_index('asin')['id'])

    # saving to PostgreSQL:
    df_products_updated.drop(columns=['id'])
    df_products_updated.to_sql(name='products', con=db.engine, index=False, if_exists="append")

    df_reviews.to_sql(name='reviews', con=db.engine, index=False, if_exists="append")

    print("celery_task_parse_csv_to_db - PASSED")
    return {'current': 100, 'total': 100, 'status': 'Парсінг Products.csv та Reviews.csv в базу PostgreSQL відбувся '
                                                    'успішно!', 'result': "Успішно!"}
