from app import app, db
from app.models import Products, Reviews


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Products': Products, 'Reviews': Reviews}
