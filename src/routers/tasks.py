import flask

from injectors import tasks

tasks_router = flask.Blueprint(
    'tasks', __name__, url_prefix='/api/tasks'
)


@tasks_router.post('/task/')
def create_task():
    ts = tasks()
    res = ts.create_task(flask.request.json)
    return flask.jsonify(res)


@tasks_router.get('/task/<int:task_id>/')
def get_task(task_id):
    ts = tasks()
    res = ts.get_task(task_id)
    return flask.jsonify(res)


@tasks_router.get('')
def get_list_tasks():
    ts = tasks()
    res = ts.get_list_tasks(
        flask.request.args.get('page', 1),
        flask.request.args.get('page_size', 100)
    )
    return flask.jsonify(res)
