from flask import current_app, Blueprint, render_template
from flask_socketio import emit
from ...extensions import socketio

bp = Blueprint('sockets', __name__)


@bp.route('/')
def index():
    return render_template('socketio.html')


@socketio.on('hello')
def handle_hello_message(message):
    current_app.logger.debug('received hello message: %s' % message)
    emit('world', 'world')
