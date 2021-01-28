import flask, datetime
from flask import request, jsonify
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['MONGODB_SETTINGS'] = {
    'db': 'Assessment',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class Task(db.DynamicDocument):
    meta = {
        'collection': 'tasks'
    }
    description = db.StringField()
    done = db.BooleanField()
    taskid = db.IntField()
    title = db.StringField()
    expiryDate = db.StringField()
    expiryTime = db.StringField()



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404



@app.route('/', methods=['GET'])
def home():
    return "<h1>Tasks</h1><p>Tasks with expiry date.</p>"


@app.route('/tasks/all', methods=['GET'])
def api_all():
    task = Task.objects()
    return jsonify(task)



@app.route('/tasks/<int:id>', methods=['GET'])
def task_filter(id):
    task = Task.objects(taskid=id).first()
    if not task:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(task)

@app.route('/tasks/create', methods=['POST'])
def create_record():
    data = request.get_json()
    task = Task(**data).save()
    id = task.id

    return {'id': str(id)}, 200


@app.route('/tasks/update/<int:id>', methods=['PUT'])
def update_record(id):
    data = request.get_json()
    Task.objects.get(taskid=id).update(**data)

    return '', 200


@app.route('/tasks/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    Task.objects.get(taskid=id).delete()
    return '', 200

@app.route('/notification', methods=['GET'])
def check_expiry():
    now = datetime.datetime.now()
    fif_minutes = datetime.timedelta(minutes=15)
    fut_time = now + fif_minutes
    exprNow = Task.objects(Q(expiryDate=fut_time.strftime("%d/%m/%Y")) & Q(expiryTime=fut_time.strftime("%H:%M")))
    if exprNow:
        for task in exprNow:
            message = ["\"" + task["title"] + "\"" + " is expiring in 15 minutes"]
            message.append("Current time is " + str(now))
        return jsonify(message)
    else:
        return ('', 204)


app.run()