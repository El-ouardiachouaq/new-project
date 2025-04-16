from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    failed_attempts = db.Column(db.Integer, default=0)
    blocked_until = db.Column(db.DateTime, nullable=True)
    reset_token = db.Column(db.String(100), unique=True)
    reset_token_expiry = db.Column(db.DateTime)
    calculations = db.relationship('Calculation', backref='user', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_blocked(self):
        return self.blocked_until and self.blocked_until > datetime.utcnow()

    def increment_failed_attempts(self):
        self.failed_attempts += 1
        if self.failed_attempts >= 3:
            self.blocked_until = datetime.utcnow() + timedelta(minutes=5 * (2 ** (self.failed_attempts // 3 - 1)))
        db.session.commit()

    def reset_failed_attempts(self):
        self.failed_attempts = 0
        self.blocked_until = None
        db.session.commit()

class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    x_A = db.Column(db.Float, nullable=False)
    D_AB0 = db.Column(db.Float, nullable=False)
    D_BA0 = db.Column(db.Float, nullable=False)
    rA = db.Column(db.Float, nullable=False)
    rB = db.Column(db.Float, nullable=False)
    D_AB_exp = db.Column(db.Float, nullable=False)
    T = db.Column(db.Float, nullable=False)
    a_AB = db.Column(db.Float, nullable=False)
    a_BA = db.Column(db.Float, nullable=False)
    q_A = db.Column(db.Float, nullable=False)
    q_B = db.Column(db.Float, nullable=False)
    result_D_AB = db.Column(db.Float, nullable=False)
    result_error = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'x_A': self.x_A,
            'D_AB0': self.D_AB0,
            'D_BA0': self.D_BA0,
            'rA': self.rA,
            'rB': self.rB,
            'D_AB_exp': self.D_AB_exp,
            'T': self.T,
            'a_AB': self.a_AB,
            'a_BA': self.a_BA,
            'q_A': self.q_A,
            'q_B': self.q_B,
            'result_D_AB': self.result_D_AB,
            'result_error': self.result_error,
            'date_created': self.date_created.isoformat()
        } 