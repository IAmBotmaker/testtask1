from celery import Celery

celery = Celery(
    'app',
    broker='pyamqp://',
    # backend='rpc://',
    backend='rpc://',
    include=['app.tasks']
)

if __name__ == '__main__':
    celery.start()
