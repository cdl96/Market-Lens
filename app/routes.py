from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Job, MarketData
from app import db, scheduler

main = Blueprint('main', __name__)

@main.route('/')
def dashboard():
    market_data = MarketData.query.order_by(MarketData.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', market_data=market_data)

@main.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if request.method == 'POST':
        job_name = request.form.get('name')
        job_function = request.form.get('function')
        job_interval = request.form.get('interval')
        
        new_job = Job(
            name=job_name,
            function=job_function,
            interval=int(job_interval)
        )
        
        db.session.add(new_job)
        db.session.commit()
        
        # Add job to scheduler
        scheduler.add_job(
            id=str(new_job.id),
            func=f'app.scheduler:{job_function}',
            trigger='interval',
            seconds=int(job_interval)
        )
        
        flash('Job created successfully!', 'success')
        return redirect(url_for('main.jobs'))
    
    jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs)
