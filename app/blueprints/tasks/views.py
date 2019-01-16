from flask import current_app, Blueprint
from ...extensions import celery

bp = Blueprint('main', __name__)


@bp.route('/add')
def add():
    current_app.logger.debug('async run add task')
    task_add.delay(123, 456)
    return 'task submit'


@celery.task
def task_add(x, y):
    current_app.logger.debug('run add task')
    return x + y
