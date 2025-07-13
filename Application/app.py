from flask import Flask, render_template_string, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import numpy as np
from deepface import DeepFace
import tempfile
import os
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple user storage (in production, use a database)
users = {}

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user_data = users[user_id]
        return User(user_id, user_data['username'], user_data['password_hash'])
    return None

# Emotion detection API route
@app.route('/api/detect', methods=['POST'])
def detect_emotion():
    if 'image' not in request.files:
        return "No image uploaded", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
        file.save(temp.name)
        temp_path = temp.name

    try:
        # Read image with OpenCV
        img = cv2.imread(temp_path)
        if img is None:
            return "Invalid image", 400

        # Use DeepFace to analyze emotion
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion'] if isinstance(result, list) else result['dominant_emotion']

        return dominant_emotion  # Return as plain text

    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        os.remove(temp_path)

# HTML templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Sproutify</title>
    <style>
        body { 
            background: linear-gradient(135deg, #e8f5e9, #a5d6a7, #43a047); 
            font-family: 'Segoe UI', sans-serif; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            min-height: 100vh; 
            margin: 0; 
        }
        .container { 
            background: rgba(255,255,255,0.95); 
            border-radius: 18px; 
            box-shadow: 0 8px 32px rgba(67,160,71,0.12); 
            padding: 32px 28px; 
            display: flex; 
            flex-direction: column; 
            align-items: center;
            min-width: 300px;
        }
        h1 { color: #2e7d32; margin-bottom: 18px; letter-spacing: 2px; }
        form { display: flex; flex-direction: column; align-items: center; width: 100%; }
        input[type="text"], input[type="password"] { 
            width: 100%; 
            padding: 12px; 
            margin: 8px 0; 
            border: 2px solid #e0e0e0; 
            border-radius: 8px; 
            font-size: 16px; 
            box-sizing: border-box;
        }
        input[type="text"]:focus, input[type="password"]:focus { 
            border-color: #43a047; 
            outline: none; 
        }
        button { 
            background: #43a047; 
            color: #fff; 
            border: none; 
            border-radius: 8px; 
            padding: 12px 28px; 
            font-size: 16px; 
            cursor: pointer; 
            transition: background 0.2s; 
            margin: 8px 0;
            width: 100%;
        }
        button:hover { background: #388e3c; }
        .error { color: #d32f2f; margin: 8px 0; text-align: center; }
        .success { color: #388e3c; margin: 8px 0; text-align: center; }
        .link { color: #43a047; text-decoration: none; margin-top: 16px; }
        .link:hover { text-decoration: underline; }
        .footer { margin-top: 32px; color: #A5D6A7; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Login to Sproutify</h1>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        {% if success %}
        <div class="success">{{ success }}</div>
        {% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <button type="submit">Login</button>
        </form>
        <a href="{{ url_for('register') }}" class="link">Don't have an account? Register here</a>
    </div>
    <div class="footer">&copy; 2024 Sproutify</div>
</body>
</html>
'''

REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - Sproutify</title>
    <style>
        body { 
            background: linear-gradient(135deg, #e8f5e9, #a5d6a7, #43a047); 
            font-family: 'Segoe UI', sans-serif; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            min-height: 100vh; 
            margin: 0; 
        }
        .container { 
            background: rgba(255,255,255,0.95); 
            border-radius: 18px; 
            box-shadow: 0 8px 32px rgba(67,160,71,0.12); 
            padding: 32px 28px; 
            display: flex; 
            flex-direction: column; 
            align-items: center;
            min-width: 300px;
        }
        h1 { color: #2e7d32; margin-bottom: 18px; letter-spacing: 2px; }
        form { display: flex; flex-direction: column; align-items: center; width: 100%; }
        input[type="text"], input[type="password"] { 
            width: 100%; 
            padding: 12px; 
            margin: 8px 0; 
            border: 2px solid #e0e0e0; 
            border-radius: 8px; 
            font-size: 16px; 
            box-sizing: border-box;
        }
        input[type="text"]:focus, input[type="password"]:focus { 
            border-color: #43a047; 
            outline: none; 
        }
        button { 
            background: #43a047; 
            color: #fff; 
            border: none; 
            border-radius: 8px; 
            padding: 12px 28px; 
            font-size: 16px; 
            cursor: pointer; 
            transition: background 0.2s; 
            margin: 8px 0;
            width: 100%;
        }
        button:hover { background: #388e3c; }
        .error { color: #d32f2f; margin: 8px 0; text-align: center; }
        .success { color: #388e3c; margin: 8px 0; text-align: center; }
        .link { color: #43a047; text-decoration: none; margin-top: 16px; }
        .link:hover { text-decoration: underline; }
        .footer { margin-top: 32px; color: #A5D6A7; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Register for Sproutify</h1>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        {% if success %}
        <div class="success">{{ success }}</div>
        {% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required />
            <input type="password" name="password" placeholder="Password" required />
            <input type="password" name="confirm_password" placeholder="Confirm Password" required />
            <button type="submit">Register</button>
        </form>
        <a href="{{ url_for('login') }}" class="link">Already have an account? Login here</a>
    </div>
    <div class="footer">&copy; 2024 Sproutify</div>
</body>
</html>
'''

MAIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion Check - Sproutify</title>
    <style>
        body { 
            background: linear-gradient(135deg, #e8f5e9, #a5d6a7, #43a047); 
            font-family: 'Segoe UI', sans-serif; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            justify-content: center; 
            min-height: 100vh; 
            margin: 0; 
        }
        .container { 
            background: rgba(255,255,255,0.95); 
            border-radius: 18px; 
            box-shadow: 0 8px 32px rgba(67,160,71,0.12); 
            padding: 32px 28px; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
        }
        .header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            width: 100%; 
            margin-bottom: 24px; 
        }
        h1 { color: #2e7d32; margin: 0; letter-spacing: 2px; }
        .user-info { 
            display: flex; 
            align-items: center; 
            gap: 16px; 
        }
        .username { color: #43a047; font-weight: bold; }
        .logout-btn { 
            background: #d32f2f; 
            color: #fff; 
            border: none; 
            border-radius: 6px; 
            padding: 8px 16px; 
            font-size: 14px; 
            cursor: pointer; 
            transition: background 0.2s; 
        }
        .logout-btn:hover { background: #b71c1c; }
        form { display: flex; flex-direction: column; align-items: center; }
        input[type="file"] { margin-bottom: 18px; }
        button { 
            background: #43a047; 
            color: #fff; 
            border: none; 
            border-radius: 8px; 
            padding: 10px 28px; 
            font-size: 18px; 
            cursor: pointer; 
            transition: background 0.2s; 
        }
        button:hover { background: #388e3c; }
        .result { margin-top: 24px; text-align: center; }
        .footer { margin-top: 32px; color: #A5D6A7; font-size: 14px; }
        img.preview { 
            max-width: 180px; 
            max-height: 180px; 
            border-radius: 12px; 
            margin-bottom: 12px; 
            box-shadow: 0 2px 8px rgba(67,160,71,0.08); 
        }
        .emotion-raw { 
            font-size: 22px; 
            color: #2e7d32; 
            margin-top: 8px; 
            font-weight: bold; 
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Sproutify Emotion Check</h1>
            <div class="user-info">
                <span class="username">Welcome, {{ current_user.username }}!</span>
                <a href="{{ url_for('logout') }}" class="logout-btn">Logout</a>
            </div>
        </div>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="photo" accept="image/*" required />
            <button type="submit">Check Emotion</button>
        </form>
        {% if emotion %}
        <div class="result">
            {% if photo_url %}<img src="{{ photo_url }}" class="preview" alt="User Photo" />{% endif %}
            <div class="emotion-raw">{{ emotion }}</div>
        </div>
        {% endif %}
    </div>
    <div class="footer">&copy; 2024 Sproutify</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    emotion = None
    photo_url = None
    if request.method == 'POST':
        file = request.files.get('photo')
        if file:
            # Direct emotion detection without external API call
            try:
                # Save to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp:
                    file.save(temp.name)
                    temp_path = temp.name

                # Read image with OpenCV
                img = cv2.imread(temp_path)
                if img is not None:
                    # Use DeepFace to analyze emotion
                    result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
                    dominant_emotion = result[0]['dominant_emotion'] if isinstance(result, list) else result['dominant_emotion']
                    emotion = dominant_emotion
                else:
                    emotion = 'Invalid image format.'
                
                # Clean up temporary file
                os.remove(temp_path)
                
            except Exception as e:
                emotion = f'Error detecting emotion: {str(e)}'
            
            # For preview, we can use data URL (not for production, but fine for demo)
            file.seek(0)
            img_bytes = file.read()
            photo_url = 'data:' + file.content_type + ';base64,' + base64.b64encode(img_bytes).decode('utf-8')
    return render_template_string(MAIN_TEMPLATE, emotion=emotion, photo_url=photo_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Find user by username
        user_id = None
        for uid, user_data in users.items():
            if user_data['username'] == username:
                user_id = uid
                break
        
        if user_id and check_password_hash(users[user_id]['password_hash'], password):
            user = User(user_id, username, users[user_id]['password_hash'])
            login_user(user)
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password'
    
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    error = None
    success = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Check if username already exists
        for user_data in users.values():
            if user_data['username'] == username:
                error = 'Username already exists'
                break
        
        if not error:
            if password != confirm_password:
                error = 'Passwords do not match'
            elif len(password) < 6:
                error = 'Password must be at least 6 characters long'
            elif len(username) < 3:
                error = 'Username must be at least 3 characters long'
            else:
                # Create new user
                user_id = str(len(users) + 1)
                password_hash = generate_password_hash(password)
                users[user_id] = {
                    'username': username,
                    'password_hash': password_hash
                }
                success = 'Registration successful! Please login.'
    
    return render_template_string(REGISTER_TEMPLATE, error=error, success=success)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) 
