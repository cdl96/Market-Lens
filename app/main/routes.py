from datetime import datetime, timedelta
from flask import jsonify, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from app.main.forms import EditProfileForm
from app.models import User
from app.main import main  
from app.models import Message

@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('home.html', title='Welcome')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@main.route('/api/users', methods=['GET'])
@login_required
def get_users():
    search_query = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 20
    current_user.update_last_login() 
    query = User.query.filter(User.id != current_user.id)
    if search_query:
        query = query.filter(User.username.ilike(f'%{search_query}%'))
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
    user_list = []
    
    for user in users.items:
        status = 'offline'
        if user.last_login:  
            if user.last_login >= five_minutes_ago:
                status = user.status if user.status in ['online', 'away', 'busy'] else 'online'
            elif user.last_login >= (datetime.utcnow() - timedelta(hours=24)):
                status = 'away'
        
        user_list.append({
            'id': user.id,
            'username': user.username,
            'status': status,
            'last_seen': user.last_login.isoformat() if user.last_login else None  
        })

    return jsonify({
        'users': user_list,
        'total': users.total,
        'pages': users.pages,
        'current_page': page
    })

@main.route('/api/users/status', methods=['POST'])
@login_required
def update_status():
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': 'Missing status'}), 400
    
    status = data['status']
    if status not in ['online', 'away', 'busy', 'offline']:
        return jsonify({'error': 'Invalid status'}), 400

    current_user.status = status
    current_user.update_last_login() 
    db.session.commit()

    return jsonify({'status': status})


@main.route('/api/messages/<int:user_id>', methods=['GET'])
@login_required
def get_messages(user_id):
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()
    
    return jsonify([{
        'id': msg.id,
        'content': msg.content,
        'sender_id': msg.sender_id,
        'timestamp': msg.timestamp.isoformat(),
        'read': msg.read
    } for msg in messages])

@main.route('/api/messages/send', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    if not data or 'receiver_id' not in data or 'content' not in data:
        return jsonify({'error': 'Missing data'}), 400
    
    message = Message(
        sender_id=current_user.id,
        receiver_id=data['receiver_id'],
        content=data['content']
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify({
        'id': message.id,
        'content': message.content,
        'sender_id': message.sender_id,
        'timestamp': message.timestamp.isoformat()
    })

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile')

@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile', form=form)



