from src.service_modules.db.conn import db

class Product_type(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    product = db.relationship('Inventory', backref= 'products')
    roles = db.relationship('Roles', backref= 'product_type')
    assign = db.relationship('Assigned', backref= 'product_type')
    status = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"Product Type '{self.id}','{self.name}', '{self.description}')"