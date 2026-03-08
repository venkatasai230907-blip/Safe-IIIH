from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import random, string
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_key = db.Column(db.String(10), unique=True)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="Pending")
    messages = db.relationship('Message', backref='report', lazy=True)
    filename = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))
    sender = db.Column(db.String(20))
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

with app.app_context():
    db.create_all()
    # Add a default admin if one doesn't exist
    if not Admin.query.first():
        db.session.add(Admin(username='user@gmail.com', password='user1234'))
        db.session.add(Admin(username='user2@gmail.com', password='user2345'))
        db.session.add(Admin(username='user3@gmail.com', password='user3456'))
        db.session.commit()

@app.route('/')
def home(): return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'admin_id' in session:
        return redirect(url_for('committee'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session['admin_id'] = admin.id
            return redirect(url_for('committee'))
        else:
            return render_template('dashboard.html', error='Invalid credentials')
    return render_template('dashboard.html')

@app.route('/committee')
def committee():
    if 'admin_id' in session:
        return render_template('committee.html')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    return redirect(url_for('admin'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/emergency_numbers')
def emergency_numbers():
    return render_template('emergency_numbers.html')

@app.route('/api/report', methods=['POST'])
def create_report():
    if request.is_json:
        data = request.get_json()
        category = data.get('category')
        description = data.get('description')
        filename = None
    else:
        category = request.form.get('category')
        description = request.form.get('description')
        file = request.files.get('file')
        filename = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    key = 'SAFE-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    new_report = Report(case_key=key, category=category, description=description, filename=filename)
    db.session.add(new_report)
    db.session.commit()
    return jsonify({"case_key": key})

@app.route('/api/chat/<key>', methods=['GET', 'POST'])
def chat(key):
    report = Report.query.filter_by(case_key=key).first_or_404()
    if request.method == 'POST':
        msg = Message(report_id=report.id, sender=request.json['sender'], text=request.json['text'])
        db.session.add(msg)
        db.session.commit()

    msgs = [{"sender": m.sender, "text": m.text, "timestamp": m.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for m in report.messages]
    return jsonify({
        "status": report.status, 
        "messages": msgs, 
        "description": report.description, 
        "filename": report.filename,
        "resolved_at": report.resolved_at.strftime("%Y-%m-%d %H:%M:%S") if report.resolved_at else None
    })

@app.route('/api/admin/all')

def get_all():

    all_r = Report.query.all()

    return jsonify([{"key": r.case_key, "cat": r.category, "status": r.status, "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")} for r in all_r])



@app.route('/api/get_committee_html')

def get_committee_html():

    all_r = Report.query.all()

    return render_template('committee.html', data=all_r)



@app.route('/api/resolve/<key>', methods=['POST'])

def resolve_report(key):

    report = Report.query.filter_by(case_key=key).first_or_404()

    report.status = "Resolved ✅"

    report.resolved_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"status": "success"})



if __name__ == '__main__':



    app.run(debug=True, port=5001)