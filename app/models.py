from app import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    # status = db.Column(db.String(20), default='offline')  # 'online', 'offline', 'away', 
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# class Message(db.Model):
#     __tablename__ = 'messages'
    
#     id = db.Column(db.Integer, primary_key=True)
#     sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     read = db.Column(db.Boolean, default=False)

#     sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
#     receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')

class Stock(db.Model):
    __tablename__ = 'stocks'
    stock_time = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)
    ticker = db.Column(db.String(20), primary_key=True)
    company_name = db.Column(db.String(120), unique=True, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, nullable=False)
    day_low = db.Column(db.Float, nullable=False)
    day_high = db.Column(db.Float, nullable=False)
    year_low = db.Column(db.Float, nullable=False)
    year_high = db.Column(db.Float, nullable=False)

class WatchList(db.Model):
    __tablename__ = "watchlists"
    watchlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to users table
    ticker = db.Column(db.String(20), nullable=False)  # Ticker column
    added_date = db.Column(db.DateTime, default=datetime.utcnow)  # Date added, default is current time
    # Define the relationship to the User model (if necessary)
    user = db.relationship('User', backref=db.backref('watchlists'))

    def __repr__(self):
        return f'<Watchlist {self.watchlist_id} - {self.ticker}>'


class Articles(db.Model):
    __tablename__ = "articles"
    article_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    source = db.Column(db.String(20), unique=True, nullable=False)
    url = db.Column(db.String(20), unique=True, nullable=False)
    article_date = db.Column(db.DateTime, default=datetime.utcnow)