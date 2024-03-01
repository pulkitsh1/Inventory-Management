from src.service_modules.db.conn import db

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(80),nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))
    assigned = db.relationship('Assigned',backref='product')
    status = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Inventory '{self.product_name}','{self.price}', '{self.quantity}','{self.product_type_id}','{self.status}')"
    
    
    