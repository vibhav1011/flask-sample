from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# from models import db, EmployeeInfo

from flask_migrate import Migrate
from sqlalchemy import inspect
import logging

logging.basicConfig(filename="employee.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:work123@localhost:5432/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)
db = SQLAlchemy(app)


class EmployeeInfo(db.Model):
    __tablename__ = 'EmployeeInfo'

    employee_id = db.Column(db.Integer, unique=True, primary_key=True)
    employee_name = db.Column(db.String(50))
    employee_age = db.Column(db.Integer)

    def __init__(self, employee_name, employee_age):
        self.employee_name = employee_name
        self.employee_age = employee_age

    def __repr__(self):
        return f"{self.employee_name} : {self.employee_age}"


migrate = Migrate(app, db)


def sqlachemy_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def work():
    if request.method == 'GET':
        try:
            name = request.headers.get("name")
            search_employee = EmployeeInfo.query.filter_by(employee_name=name).first()
            response = sqlachemy_as_dict(search_employee)
            return jsonify(response.get("employee_age"))

        except Exception as e:
            logger.exception("Error retrieving employee_name")
            return "Expected format :\n curl -X GET url -H \"name\":\"employee_name\"\n", e

    if request.method == 'POST':
        try:
            name = request.headers.get("name")
            age = request.headers.get("age")
            new_employee = EmployeeInfo(employee_name=name, employee_age=age)
            db.session.add(new_employee)
            db.session.commit()
            return 'Employee added successfully!'

        except Exception as e:
            logger.exception("Error adding employee")
            return "Expected format :\n curl -X POST url -H \"name\":\"employee_name\" -H \"age\":\"employee_age\"\n", e

    if request.method == 'DELETE':
        try:
            name = request.headers.get("name")
            ex_employee = EmployeeInfo.query.filter_by(employee_name=name).first()
            EmployeeInfo.delete(ex_employee)
            db.session.commit()
            return "Employee removed successfully!"

        except Exception as e:
            logger.exception("Error removing employee")
            return e, "Expected format :\n curl -X DELETE url -H \"name\":\"employee_name\"\n"

    else:
        return "Error! Invalid request."


if __name__ == '__main__':
    app.run(debug=True)


# postgres pw : work123
