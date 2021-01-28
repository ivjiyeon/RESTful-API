import flask
from flask import request, jsonify, json
from flask_mongoengine import MongoEngine


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
    # record = json.loads(request.data)
    # task = Task(taskid=record['id'],
    #             description=record['description'],
    #             title=record['title'],
    #             done=record['done'],
    #             expiryDate=record['expiryDate'],
    #             expiryTime=record['expiryTime'])
    # task.save()
    # return jsonify(task)

@app.route('/tasks/update/<int:id>', methods=['PUT'])
def update_record(id):
    data = request.get_json()
    Task.objects.get(taskid=id).update(**data)

    return '', 200
    # record = json.loads(request.data)
    # task = Task.objects(taskid=record['id']).first()
    # if not task:
    #     return jsonify({'error': 'data not found'})
    # else:
    #     task.update(expiryTime=record['expiryTime'])
    # return jsonify(task)

@app.route('/tasks/delete/<int:id>', methods=['DELETE'])
def delete_record(id):
    Task.objects.get(taskid=id).delete()
    return '', 200

    # record = json.loads(request.data)
    # task = Task.objects(taskid=record['id']).first()
    # if not task:
    #     return jsonify({'error': 'data not found'})
    # else:
    #     task.delete()
    # return jsonify(task)

app.run()