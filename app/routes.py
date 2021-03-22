from app import app


@app.route('/')
@app.route('/index')
def index():
    return "Just a blank root route"
