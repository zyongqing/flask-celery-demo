from flask import current_app, Blueprint
from ...extensions import celery

bp = Blueprint('main', __name__)


@bp.route('/add')
def add():
    current_app.logger.debug('async run add task')
    task_add.delay(123, 456)
    return 'task submit'


@bp.route('/sub')
def sub():
    current_app.logger.debug('async run sub task')
    task_sub.delay(456, 123)
    return 'task submit'


# default queue is: celery
# celery -A manage.celery worker -c 1 --loglevel=debug
@celery.task()
def task_add(x, y):
    current_app.logger.debug('run add task')
    return x + y


# need specified parameter: -Q
# celery -A manage.celery worker -c 1 -Q high --loglevel=debug
@celery.task(queue='high')
def task_sub(x, y):
    current_app.logger.debug('run sub task')
    return x - y
