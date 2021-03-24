1. For asyncronous requests:
   a) drop all tables in PostgreSQL and
   b) create_all tables in PostgreSQL
   (which could take relatively long time) - celery is used
In order to run celery worker in debug mode after celery was installed from pypi, run in bash in the root directory of the application:
   ./venv/bin/celery -A app.celery worker --without-heartbeat --without-gossip --without-mingle --pool=prefork --loglevel=debug -n worker_1 -E
    For celery pyamqp broker and rpc backend for development environment is used   

2. For GET endpoints two approaches were made:
   a) Jinja rendering, including pagination 
   This one is non-cached
   b) Creation of REST API for GET requests with pagination
   For this endpoint REDIS cache is applied (for it to work you need to have a redis-server running in your environment/server)
   
3. In config.py (.gitignored) default values for pagination and maximum number of reviews served:
    REVIEWS_PER_PAGE = 2 # pagination parameter, number of reviews per page
    REVIEWS_MAX = 20  # pagination parameter, maximum number of reviews to be provided
   
4. Pagination works as follows:
http://localhost:5000/api/get-endpoint-json/id?page=page_number 
   OR 
http://localhost:5000/api/get-endpoint-json/id (default for page=1)
where 
   id - is product id
   page_number - is number of page (optional argument for the page #1)
   