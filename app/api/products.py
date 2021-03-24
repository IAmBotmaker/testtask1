from app import app
from app.api import bp
import collections
from flask import jsonify, request, abort
from app.models import Products
#from .errors import error_response


def get_paginated_list(klass, url, page, per_page, limit, id):
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for f in range(0, len(lst), n):
            yield lst[f:f + n]

    if (page <= 0):
        abort(404)
        #error_response(404)

    # check if page exists
    product_obj_instance = klass.query.get_or_404(id)

    # get raw reviews list
    reviews_list = product_obj_instance.reviews.all()
    # number of raw reviews
    reviews_list = reviews_list[:limit]
    count = len(reviews_list)

    # prepare list of reviews for selected page
    list_of_chunks = list(chunks(reviews_list, per_page))
    number_of_pages = len(list_of_chunks)
    # if requested page number is larger than number of pages
    if (page > number_of_pages):
        abort(404)
        #error_response(404)
    reviews_list_selected_page = list_of_chunks[page - 1]

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
    obj['results'] = []

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
    list_of_reviews = []
    list_of_reviews_dic = {"title": "",
                           "review": ""}
    for i in range(len(reviews_list_selected_page)):
        list_of_reviews_dic["title"] = reviews_list_selected_page[i].title
        list_of_reviews_dic["review"] = reviews_list_selected_page[i].review
        list_of_reviews.append(list_of_reviews_dic.copy())

    obj['results'] = list_of_reviews
    return obj


@bp.route('/get-endpoint-json/<int:num>', methods=['GET'])
def get_endpoint_specific_json(num):
    result = get_paginated_list(
        Products,
        '/get-endpoint-json/' + str(num),
        page=request.args.get('page', 1, type=int),
        per_page=app.config['REVIEWS_PER_PAGE'],
        limit=app.config['REVIEWS_MAX'],
        id=num)
    return jsonify(result)  # does not keep order, but beautified
    # return json.dumps(result)  # does keep order
