import time
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


@bp.route('/mul')
def mul():
    current_app.logger.debug('async run mul task')
    task_mul.delay(456, 123)
    return 'task submit'


@bp.route('/div')
def div():
    current_app.logger.debug('async run div task')
    task_div.delay(456, 0)
    return 'task submit'


@bp.route('/ack_before')
def ack_before():
    current_app.logger.debug('async run ack_before task')
    task_ack_before.delay()
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


# bind means task instance itself as first argument
@celery.task(bind=True)
def task_mul(self, x, y):
    current_app.logger.debug('run mul task: %s' % self.request.id)
    return x * y


# retry task musts be a bind task
# when task retry it will send a new message with same task id and arguments
# http://docs.celeryproject.org/en/latest/userguide/tasks.html#retrying
@celery.task(bind=True, max_retries=1)
def task_div(self, x, y):
    try:
        current_app.logger.debug('run div task: %s' % self.request.id)
        return x / y
    except Exception as e:
        current_app.logger.warn(e)
        time.sleep(5)
        y += 1  # when retried y will not changed, still be 0
        raise self.retry(exc=e, countdown=60)  # retry as a exception
        current_app.logger.debug('this line does not show')


# in default, task ack message before it is executed
# when any exception raise, it was gone and never process again
# if task is idempotent you can set option: acks_late
@celery.task
def task_ack_before():
    current_app.logger.debug('run ack_before task')
    time.sleep(5)
    raise Exception('something wrong')
