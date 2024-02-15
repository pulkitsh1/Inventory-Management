from src.service_modules.db.conn import db

class Inventory(db.Model):
    product_name = db.Column(db.String(80), primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Inventory '{self.product_name}','{self.price}', '{self.quantity}','{self.product_type}')"