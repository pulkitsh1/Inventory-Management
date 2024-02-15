from src.service_modules.db.conn import db
from datetime import datetime

class TransactionsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(80), nullable=False)
    price_per_unit = db.Column(db.Integer, nullable=True)
    total_price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String(120), nullable=False)
    order_placement_date = db.Column(db.Date, default=datetime.utcnow)
    transaction_id = db.Column(db.Integer, nullable=True)
    attachments = db.Column(db.String(256), nullable=True)
    order_status = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Transaction '{self.product_name}','{self.price_per_unit}', '{self.total_price}','{self.quantity}','{self.product_type}','{self.order_placement_date}', '{self.transaction_id}','{self.attachments}','{self.order_status}')"