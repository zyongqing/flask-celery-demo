import coloredlogs
from flask import Flask
from config import config
from .extensions import celery, socketio


def _init_logging(app):
    LOG_FORMAT = '%(levelname)s\t%(asctime)s\t%(message)s'
    if not app.debug:
        coloredlogs.install(fmt=LOG_FORMAT, level='WARN', logger=app.logger)

    else:
        coloredlogs.install(fmt=LOG_FORMAT, level='DEBUG', logger=app.logger)


def _init_errors(app):
    @app.errorhandler(403)
    def page_permission_deny(e):
        return '403', 403

    @app.errorhandler(404)
    def page_not_found(e):
        return '404', 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return '500', 500


def _init_extensions(app):
    celery.init_app(app)
    socketio.init_app(app)


def _register_blueprints(app):
    from .blueprints.tasks.views import bp
    app.register_blueprint(bp, url_prefix='/tasks')

    from .blueprints.sockets.views import bp
    app.register_blueprint(bp, url_prefix='/sockets')


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py', silent=True)

    _init_logging(app)
    _init_errors(app)
    _init_extensions(app)
    _register_blueprints(app)

    return app
