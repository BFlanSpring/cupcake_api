"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cupcake(db.Model):
    """Cupcakes"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, 
                    primary_key=True,
                    autoincrement=True)
    flavor = db.Column(db.Text,
                        nullable=False)
    size = db.Column(db.Text,
                        nullable=False) 
    rating = db.Column(db.Float,
                        nullable=True) 
    image = db.Column(db.Text,  
                        nullable=True,
                        default = "https://tinyurl.com/demo-cupcake")

    def serialize(self):
        return {
            'id':self.id,
            'flavor':self.flavor,
            'size':self.size,
            'rating':self.rating,
            'image':self.image
        }  


def connect_db(app):
    db.app = app
    with app.app_context():
        db.create_all()
