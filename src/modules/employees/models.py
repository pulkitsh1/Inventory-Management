from src.service_modules.db.conn import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    employee_id = db.Column(db.Integer, nullable=True)
    assigned = db.relationship('Assigned',backref='employee')
    status =  db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Employee('{self.id}','{self.name}', '{self.email}', '{self.employee_id}','{self.status}')"