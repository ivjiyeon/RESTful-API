# RESTful-API  
Simple RESTful API created with Python, Flask and MongoDB  
  
## Table of Contents  
* [Aim](#Aim)  
* [Database](#Database)
* [Requirements](#Requirements)
* [Usage](#Usage)

## Aim  
This project is simple task management system with the following functionalities:  
* View tasks  
* Filter tasks  
* Create tasks  
* Update tasks  
* Delete tasks
* Notify user before task expires using client-side logger  
  
## Database  
The data is stored in MongoDB database with the following schematic:  
```
{
    "_id": {
        "$oid": <MongoDB objectID(string)>
    },
    "description": <description(string)>,
    "done": <status(boolean)>,
    "title": <task title(string)>,
    "expiryDate": <DD/MM/YYYY (string)>,
    "expiryTime": <HH:MM (string)>,
    "taskid": <id (integer)>
}
```
  
## Requirements  
* Python 3.8.3  
* Flask 1.1.2
* MongoEngine 0.22.1  
* flask_mongoengine 1.0.0  
* MongoDB 4.4  
  
## Usage  
### Without connecting database 
1. Start the flask server  
    ```
    python api.py
    ```
2. Start the logger on the client-side 
If the task is about to expire in 15 minutes, a notification will appear on the logger screen.
    ```
    python logger.py
    ```
3. Home page  
    ```
    curl -i http://localhost:5000/
    ```
3. Show all tasks  
    ```
    curl -i http://localhost:5000/tasks/all
    ```
4. Filter task by taskID  
    ```
    curl -i http://localhost:5000/tasks/<taskID>
    ```
5. Create task  
Title is mandatory. All the other fields are optional.
    ```
    curl -i -H "Content-Type:application/json" -X POST -d "{\"title\":<title>}" http://localhost:5000/tasks/create
    ```
6. Update task with taskID
    ```
    curl -i -H "Content-Type: application/json" -X PUT -d "{<field name>:<field value>}" http://127.0.0.1:5000/tasks/update/<taskID>
    ```
7. Delete task with taskID
    ```
    curl -i -X DELETE http://127.0.0.1:5000/tasks/delete/<taskID>
    ```
  
### With connecting database  
1. Start MongoDB server  
  1.1 In MongoDB server, create a database called 'Assessment'  
  1.2 Inside the 'Assessment', create a collection called 'tasks'. Optionally, you can import the provided tasks_mgoDB.json file
1. Start the flask server  
    ```
    python DBconnectedAPI.py
    ```
2. Start the logger on the client-side 
If the task is about to expire in 15 minutes, a notification will appear on the logger screen.
    ```
    python logger.py
    ```
3. Home page  
    ```
    curl -i http://localhost:5000/
    ```
3. Show all tasks  
    ```
    curl -i http://localhost:5000/tasks/all
    ```
4. Filter task by taskID  
    ```
    curl -i http://localhost:5000/tasks/<taskID>
    ```
5. Create task  
Title is mandatory. All the other fields are optional.
    ```
    curl -H "Content-Type: application/json" -X POST -d "{\"taskid\":<taskID>, \"description\":<description>, \"title\":<title>, \"done\":<status>, \"expiryDate\":<DD/MM/YYYY>, \"expiryTime\":<HH:MM>}" http://localhost:5000/tasks/create
    ```
6. Update task with taskID
    ```
    curl -H "Content-Type: application/json" -X PUT -d "{<field name>:<field value>}" http://localhost:5000/tasks/update/<taskID>
    ```
7. Delete task with taskID
    ```
    curl -i -X DELETE http://localhost:5000/tasks/delete/<taskID>
    ```
