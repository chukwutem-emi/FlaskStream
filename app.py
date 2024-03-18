from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///source.db"
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    

def __repr__ (self):
    return self.name 
 
app.app_context().push()


taskField = {
    "id": fields.Integer,
    "name": fields.String
  }


class items(Resource):
    @marshal_with(taskField)
    def get(self):
          task = Task.query.all()
          return task
      
    
    @marshal_with(taskField)
    def post(self):
        data = request.json
        task = Task(name=data["name"])
        db.session.add(task)
        db.session.commit()

        task = Task.query.all()
        return task
       


class item(Resource):
    @marshal_with(taskField)
    def get(self, pk):
        # return fakedatabase[pk]
         task = Task.query.filter_by(id=pk).first()
         return task
       
    
    # @marshal_with(taskField)
    def put(self, pk):
        data = request.json
        task = Task.query.filter_by(id=pk).first()
        task.name = data["name"]
        
        return task
       
    
    # @marshal_with(taskField)
    def delete(self, pk):
        task = Task.query.filter_by(id=pk).first()
        db.session.delete(task)
        db.session.commit() 

        task = Task.query.all()
        return task
       

api.add_resource(items, "/")
api.add_resource(item, "/<int:pk>")

if __name__ == "__main__":
    app.run(debug=True)
    