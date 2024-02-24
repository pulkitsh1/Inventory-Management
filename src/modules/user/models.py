from src.service_modules.db.conn import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.relationship('Roles', backref='user')
    status =  db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"User('{self.id}','{self.name}', '{self.email}')"
    

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey('product_type.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Roles '{self.id}','{self.product_type_id}', '{self.name}')"
    


