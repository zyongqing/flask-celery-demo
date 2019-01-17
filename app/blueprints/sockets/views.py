import time
from flask import current_app, Blueprint, render_template, request, url_for
from flask_socketio import emit
from requests import post
from ...extensions import celery, socketio

bp = Blueprint('sockets', __name__)


@bp.route('/')
def index():
    return render_template('socketio.html')


@bp.route('/send')
def send():
    socketio.emit('world', 'new world')
    return 'message sent'


@bp.route('/submit_task')
def submit_task():
    callback_url = url_for('.update_task_status', _external=True)
    current_app.logger.debug(callback_url)
    task_do_something.delay(url_for('.update_task_status', _external=True))
    return 'task submit'


@bp.route('/update_task_status', methods=['POST'])
def update_task_status():
    data = request.json
    socketio.emit('world', data)
    return 'task status update'


@socketio.on('hello')
def handle_hello_message(message):
    current_app.logger.debug('received hello message: %s' % message)
    emit('world', 'world')


@celery.task(bind=True)
def task_do_something(self, url):
    current_app.logger.debug('run do_something task')
    for i in range(10):
        progress = 1/10 * i
        post(url, json={'task': self.request.id, 'status': progress})
        time.sleep(1)
    post(url, json={'task': self.request.id, 'status': 'done'})
