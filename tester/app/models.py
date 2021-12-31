from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
