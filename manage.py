import os
from app import create_app, celery

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
celery = celery


@app.shell_context_processor
def make_shell_context():
    context = dict(app=app)
    return context
