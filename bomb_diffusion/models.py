from datetime import datetime
from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    
    puzzles = db.relationship('Puzzle', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def get_completion_time(self):
        if not self.end_time or not self.start_time:
            return None
        duration = self.end_time - self.start_time
        return str(duration).split('.')[0]

    def __repr__(self):
        return f'<User {self.username}>'

class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, index=True)
    input_data = db.Column(db.Text)
    solution = db.Column(db.String(256))
    is_solved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Puzzle Level {self.level} for User {self.user_id}>'