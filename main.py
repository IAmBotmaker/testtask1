from app import app, db, redis_client
from app.models import Products, Reviews


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Products': Products, 'Reviews': Reviews, 'redis_client': redis_client}

