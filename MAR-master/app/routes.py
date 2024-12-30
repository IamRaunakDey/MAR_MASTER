# import os
# from flask import render_template, flash, redirect, url_for, request, session
# from app import app
# from app.models import users
# from flask import render_template, flash, redirect, url_for, request, session, current_app
# from flask_mail import Mail, Message
# from app.models import users
# import secrets

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# @app.route('/')
# def home():
#     return render_template('home.html')
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = users.get(username)
#         if user and user.check_password(password):
#             session['username'] = username
#             session['role'] = user.role
#             return redirect(url_for('upload'))
#         else:
#             flash('Invalid username or password')
#     return render_template('login.html')

# @app.route('/submission', methods=['GET', 'POST'])
# def upload():
#     if 'username' not in session:
#         return redirect(url_for('login'))
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             student_id = request.form['student_id']
#             filename = f"{student_id}_{file.filename}"
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             flash('File successfully uploaded')
#     return render_template('submission.html')

# @app.route('/admin')
# def admin():
#     if 'username' not in session and session['role'] != 'admin':
#         return redirect(url_for('login'))
#     files = os.listdir(app.config['UPLOAD_FOLDER'])
#     return render_template('admin.html', files=files)






# # mail = Mail(app)

# def send_reset_email(user_email):
#     token = secrets.token_urlsafe(16)
#     reset_url = url_for('reset_password', token=token, _external=True)
#     msg = Message('Password Reset Request', sender='noreply@yourdomain.com', recipients=[user_email])
#     msg.body = f"""To reset your password, visit the following link:
# {reset_url}
# If you did not make this request, simply ignore this email and no changes will be made.
# """
#     mail.send(msg)

# @app.route('/forgot_password', methods=['GET', 'POST'])
# def forgot_password():
#     if request.method == 'POST':
#         email = request.form['email']
#         user = next((user for user in users.values() if user.email == email), None)
#         if user:
#             send_reset_email(user.email)
#             flash('An email has been sent with instructions to reset your password.', 'info')
#         else:
#             flash('Email address not found.', 'danger')
#     return render_template('forgot_password.html')

# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if request.method == 'POST':
#         password = request.form['password']
#         user_email = 'extracted from token (implement your logic)'
#         user = next((user for user in users.values() if user.email == user_email), None)
#         if user:
#             user.password_hash = generate_password_hash(password)
#             flash('Your password has been updated!', 'success')
#             return redirect(url_for('login'))
#         else:
#             flash('Invalid or expired token.', 'danger')
#     return render_template('reset_password.html')

import os
import secrets
from flask import Flask, render_template, flash, redirect, url_for, request, session
from werkzeug.security import generate_password_hash
from flask_mail import Mail, Message
from app import app
from app.models import users  # Assuming users is a dictionary or ORM model
submission_data = []

# Flask app configuration
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'png', 'jpg'}
app.secret_key = 'your-secret-key'

# Mail configuration (adjust as needed)
mail = Mail(app)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)  # Retrieve user data
        if user and user.check_password(password):
            session['username'] = username
            session['role'] = user.role
            session['user_logged_in'] = True
            print(session)
            if user.role == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('upload'))
           # return redirect(url_for('upload'))
        else:
            print(user,user.password,password)
            flash('Invalid username or password', 'danger')
    return render_template('login.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle file uploads."""
    if 'username' not in session:
        return redirect(url_for('login'))
    if not session.get('user_logged_in') or session.get('role') != 'student':
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Validate file upload
        if 'file' not in request.files:
            flash('No file part', 'warning')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'warning')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Extract form data
            student_id = request.form.get('serial')
            activity = request.form.get('activity')
            duration = request.form.get('duration')
            points = request.form.get('points')
            participated = request.form.get('participated')
            total_points = request.form.get('t_points')

            # Ensure all required fields are present
            # if not student_id or not activity or not duration or not points or not participated or not total_points:
            #     print('enter 3')
            #     flash('All fields are required.', 'danger')
            #     return redirect(request.url)

            # Save the uploaded file
            filename = f"{student_id}_{file.filename}"
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure directory exists
            file.save(upload_path)

            # Save submission details
            submission_data.append({
                'student_id': student_id,
                'activity': activity,
                'duration': duration,
                'points': points,
                'participated': participated,
                'total_points': total_points,
                'file': filename,
            })
            print('enter 4')
            flash('File successfully uploaded', 'success')
            return redirect(url_for('home'))  # Refresh page after submission

    return render_template('upload.html')
# @app.route('/submission', methods=['GET', 'POST'])
# def upload():
#     """Handle file uploads."""
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part', 'warning')
#             return redirect(request.url)

#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file', 'warning')
#             return redirect(request.url)

#         if file and allowed_file(file.filename):
#             student_id = request.form.get('student_id')
#             if not student_id:
#                 flash('Student ID is required', 'warning')
#                 return redirect(request.url)

#             filename = f"{student_id}_{file.filename}"
#             upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Ensure directory exists
#             file.save(upload_path)
#             flash('File successfully uploaded', 'success')
#     return render_template('submission.html')

@app.route('/admin')
def admin():
    """Admin page to view uploaded files."""
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)  # Ensure directory exists
    files = os.listdir(upload_folder)
    return render_template('admin.html', files=files,submission_data=submission_data)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password requests."""
    if request.method == 'POST':
        email = request.form['email']
        user = next((user for user in users.values() if user.email == email), None)
        if user:
            send_reset_email(user.email)
            flash('An email has been sent with instructions to reset your password.', 'info')
        else:
            flash('Email address not found.', 'danger')
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset requests."""
    if request.method == 'POST':
        password = request.form['password']
        # Extract user email from the token (implement logic as needed)
        user_email = 'extracted_from_token@example.com'  # Example placeholder
        user = next((user for user in users.values() if user.email == user_email), None)
        if user:
            user.password_hash = generate_password_hash(password)
            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or expired token.', 'danger')
    return render_template('reset_password.html')

def send_reset_email(user_email):
    """Send a password reset email to the user."""
    token = secrets.token_urlsafe(16)
    reset_url = url_for('reset_password', token=token, _external=True)
    msg = Message('Password Reset Request', sender='noreply@yourdomain.com', recipients=[user_email])
    msg.body = f"""To reset your password, visit the following link:
{reset_url}
If you did not make this request, simply ignore this email and no changes will be made.
"""
    mail.send(msg)
# @app.before_request
# def session_check():
#     """Redirect to login if user is not authenticated."""
#     allowed_routes = ['login', 'logout']
#     if 'username' not in session and request.endpoint not in allowed_routes:
#         return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    """Log out the user and clear the session."""
    session.pop('user_logged_in', None)
    session.pop('user_role', None)
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


