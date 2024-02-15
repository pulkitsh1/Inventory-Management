from src.service_modules.db.conn import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    product_type = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f"User('{self.id}','{self.name}', '{self.email}')"

