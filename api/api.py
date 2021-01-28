import datetime, logging

import flask
from flask import request, jsonify, abort
from requests import session

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
tasks = [
    {"description": "Need to find a good Python tutorial on the web",
     "done": False,
     "id": 0,
     "title": "Learn Python",
     "expiryDate": "01/01/2021",
     "expiryTime": "20:44"},
    {"description": "Milk, Cheese, Pizza, Fruit, Tylenol",
     "done": False,
     "id": 1,
     "title": "Buy groceries",
     "expiryDate": "27/01/2021",
     "expiryTime": "20:17"},
]

@app.route('/', methods=['GET'])
def home():
    return "<h1>Tasks</h1><p>Tasks with expiry date.</p>"

@app.route('/tasks', methods=['GET'])
def name():
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def task_id(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

    # # Check if an ID was provided as part of the URL.
    # # If ID is provided, assign it to a variable.
    # # If no ID is provided, display an error in the browser.
    # if 'id' in request.args:
    #     id = int(request.args['id'])
    # else:
    #     return "Error: No id field provided. Please specify an id."
    #
    # # Create an empty list for our results
    # results = []
    #
    # # Loop through the data and match results that fit the requested ID.
    # # IDs are unique, but other fields might return many results
    # for task in tasks:
    #     if task['id'] == id:
    #         results.append(task)
    #
    # if results == []:
    #     abort(404)
    # # Use the jsonify function from Flask to convert our list of
    # # Python dictionaries to the JSON format.
    # return jsonify(results)

@app.route('/tasks/create', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)

    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': request.json.get('done', ""),
        'expiryDate': request.json.get('expiryDate', ""),
        'expiryTime': request.json.get('expiryTime', "")
    }

    tasks.append(task)
    return jsonify(tasks), 201

@app.route('/tasks/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    if 'expiryDate' in request.json and type(request.json['expiryDate']) is not unicode:
        abort(400)
    if 'expiryTime' in request.json and type(request.json['expiryTime']) is not unicode:
        abort(400)


    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    task[0]['expiryDate'] = request.json.get('expiryDate', task[0]['expiryDate'])
    task[0]['expiryTime'] = request.json.get('expiryTime', task[0]['expiryTime'])
    return jsonify({'task': task[0]})

@app.route('/tasks/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

@app.route('/notification', methods=['GET'])
def check_expiry():
    now = datetime.datetime.now()
    fif_minutes = datetime.timedelta(minutes=15)
    fut_time = now + fif_minutes
    exprSoon = [task for task in tasks if fut_time.strftime("%d/%m/%Y") == task['expiryDate']]
    exprNow = [task for task in exprSoon if fut_time.strftime("%H:%M") == task['expiryTime']]
    if len(exprNow) == 0:
        return ('', 204)
    else:
        for task in exprNow:
            message = ["\"" + task["title"] + "\"" + " is expiring in 15 minutes"]
            message.append("Current time is " + str(now))
        return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True)