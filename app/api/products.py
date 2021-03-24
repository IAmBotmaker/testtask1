import json
from app import app, redis_client, db
from app.api import bp
import collections
from flask import jsonify, request, abort
from app.models import Products, Reviews
from datetime import timedelta


# Pagination function
def get_paginated_list(klass, url, page, per_page, limit, id):
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for f in range(0, len(lst), n):
            yield lst[f:f + n]

    if (page <= 0):
        abort(404)

    # check if product exists in the PostgreSQL database
    product_obj_instance = klass.query.get_or_404(id)

    # get raw reviews list
    reviews_list = product_obj_instance.reviews.all()
    # number of raw reviews limited by maximum number of reviews allowed (set in config.py as REVIEWS_MAX)
    # to be served by REST API GET
    reviews_list = reviews_list[:limit]
    count = len(reviews_list)

    # prepare list of reviews for selected page
    list_of_chunks = list(chunks(reviews_list, per_page))
    number_of_pages = len(list_of_chunks)
    # if requested page number is larger than number of pages - abort
    reviews_list_selected_page = []
    if number_of_pages >= 1:
        if (page > number_of_pages and number_of_pages != 0):
            abort(404)
        else:
            reviews_list_selected_page = list_of_chunks[page - 1]
    else:
        reviews_list_selected_page = []

    # make response object - OrderedDict
    obj = collections.OrderedDict()
    obj['id'] = product_obj_instance.id
    obj['asin'] = product_obj_instance.asin
    obj['title'] = product_obj_instance.title
    obj['page'] = page
    obj['per_page'] = per_page
    obj['count'] = count
    obj['limit'] = limit
    obj['previous'] = ''
    obj['next'] = ''
    obj['reviews'] = []

    # make URLs

    # make previous url
    if page == 1:
        obj['previous'] = ''
    else:
        obj['previous'] = url + '?page=%d' % (page - 1,)

    if page == number_of_pages:
        obj['next'] = ''
    else:
        obj['next'] = url + '?page=%d' % (page + 1,)

    # finally extract result according to bounds
    if number_of_pages >= 1:
        list_of_reviews = []
        list_of_reviews_dic = {"title": "",
                               "review": ""}
        for i in range(len(reviews_list_selected_page)):
            list_of_reviews_dic["title"] = reviews_list_selected_page[i].title
            list_of_reviews_dic["review"] = reviews_list_selected_page[i].review
            list_of_reviews.append(list_of_reviews_dic.copy())

        obj['reviews'] = list_of_reviews
    else:
        obj['reviews'] = []
    return obj


@bp.route('/get-endpoint-json/<int:num>', methods=['GET'])
def get_endpoint_specific_json(num):
    page = request.args.get('page', 1, type=int)
    # creating unique redis key for product id & page number
    cached_response_redis_key = f"result_{num}_{page}"
    # REDIS cache used
    # Trying to get data from cache with unique redis key
    result = redis_client.get(cached_response_redis_key)
    if result is None:
        print("Could not find GET result in cache, REST API response served from PostgreSQL db")
        # Getting data from the PostgreSQL db
        result = get_paginated_list(
            Products,
            '/get-endpoint-json/' + str(num),
            page=request.args.get('page', 1, type=int),
            per_page=app.config['REVIEWS_PER_PAGE'],
            limit=app.config['REVIEWS_MAX'],
            id=num)
        # Saving data to cache with unique identifier for product id & page number
        redis_client.set(cached_response_redis_key, json.dumps(result))
        redis_client.expire(cached_response_redis_key, timedelta(seconds=10))
    else:
        print("Found cached GET response, serving data from REDIS")
        result = json.loads(result)

    return jsonify(result)  # does not keep order, but beautified
    # return json.dumps(result)  # does keep order


@bp.route('/put-endpoint-json/<int:num>', methods=['PUT'])
def put_endpoint_specific_json(num):
    product_id = num
    product_obj_instance = Products.query.get_or_404(product_id)
    asin = product_obj_instance.asin
    title = request.json['title']
    review = request.json['review']
    product_ids = product_id

    new_review = Reviews(asin=asin, title=title, review=review, product_ids=product_ids)
    db.session.add(new_review)
    db.session.commit()

    new_review_obj_instance = Reviews.query.order_by(-Reviews.id).filter_by(product_ids=product_ids).first().as_dict()

    return jsonify(new_review_obj_instance)