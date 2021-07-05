from app import db
from sqlalchemy.sql import func


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10000))
    progress = db.Column(db.Integer)
    status = db.Column(db.String(10000))

