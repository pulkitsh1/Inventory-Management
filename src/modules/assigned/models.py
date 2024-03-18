from src.service_modules.db.conn import db
from datetime import datetime

class Assigned(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('inventory.id'),nullable=True)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'),nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    assignment_date = db.Column(db.Date, default=datetime.utcnow)
    return_date = db.Column(db.Date,nullable=True)
    unique_code = db.Column(db.String(160),nullable=True)
    status = db.Column(db.TEXT, nullable=True)