from app import app
from flask import render_template, jsonify, url_for
from .tasks import celery_task_del_table_content, celery_task_parse_csv_to_db


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/clear-db', methods=['GET', 'POST'])
def clear_db():
    task1_command = celery_task_del_table_content.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus1', task_id=task1_command.id)}


@app.route('/parse-csv', methods=['GET', 'POST'])
def parse_csv():
    task2_command = celery_task_parse_csv_to_db.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus2', task_id=task2_command.id)}

@app.route('/get-endpoint-init', methods=['GET', 'POST'])
def get_endpoint():
    #task3_command = celery_task_get_endpoint.apply_async()
    return render_template('get-endpoint.html')

@app.route('/put-endpoint-init', methods=['GET', 'POST'])
def put_endpoint():
    #task4_command = celery_task_put_endpoint.apply_async()
    return render_template('put-endpoint.html')


@app.route('/status1/<task_id>')
def taskstatus1(task_id):
    task = celery_task_del_table_content.AsyncResult(task_id)
    print('task.state_1: ', task.state)
    print('task.result_1: ', task.result)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Підготовка до очищення бази даних PostgreSQL...'
        }
    elif task.state == 'RETRY':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Пробуємо відновити роботу...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

@app.route('/status2/<task_id>')
def taskstatus2(task_id):
    task = celery_task_parse_csv_to_db.AsyncResult(task_id)
    print('task.state_2: ', task.state)
    print('task.result_2: ', task.result)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Підготовка до парсингу даних з csv файлів...'
        }
    elif task.state == 'RETRY':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Пробуємо відновити роботу...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
