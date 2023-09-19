from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
app.app_context().push()

class TodoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String(200))
	summary = db.Column(db.String(200))

#db.create_all()

Resource_fields = {
	id:fields.Integer,
	'task':fields.String,
	'summary':fields.String
}

task_post_args = reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help='Task is required', required=True)
task_post_args.add_argument('summary', type=str, help='summary is required', required=True)
task_update_args = reqparse.RequestParser()
task_update_args.add_argument('task', type=str)
task_update_args.add_argument('summary', type=str)


class TodoList(Resource):
	@marshal_with(Resource_fields)
	def get(self):
		tasks = TodoModel.query.all()
		print(tasks)
		todos = {}
		for task in tasks:
			todos[task.id] = {"task":task.task, "summary": task.summary}
		print(todos)
		return todos.json()


class Todo(Resource):
	@marshal_with(Resource_fields)
	def get(self, todo_id):
		args = task_post_args.parse_args()
		task = TodoModel.query.filter_by(id = todo_id).first()
		if not task:
			abort(404, message="Could not find the task with id")
		return task


	@marshal_with(Resource_fields)
	def post(self, todo_id):
		args = task_post_args.parse_args()
		task = TodoModel.query.filter_by(id = todo_id).first()
		if task:
			abort(409, message='The Id already Taken')

		todo = TodoModel(id = todo_id, task = args['task'], summary = args['summary'])
		db.session.add(todo)
		db.session.commit()
		return todo, 201

	@marshal_with(Resource_fields)
	def put(self, todo_id):
		args = task_update_args.parse_args()
		task = TodoModel.query.filter_by(id = todo_id).first()
		if not task:
			abort (404, message="Task does not exist")
		if args['task']:
			todo = TodoModel(task = args['task'])
		if args['summary']:
			todo = TodoModel(summary = args['summary'])
		db.session.add()
		db.session.commit()
		return task, 201

	def delete(self,todo_id):
		task = TodoModel.query.filter_by(id = todo_id).first()
		if not task:
			abort (404, message="Can not delete task does not exist")
		db.session.delete(task)
		db.session.commit()
		return todos, 201
		



api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<int:todo_id>')

if __name__ == '__main__':
	app.run(debug=True)
