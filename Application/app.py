from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# HTML template for the frontend
TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion Check - Sproutify</title>
    <style>
        body { background: linear-gradient(135deg, #e8f5e9, #a5d6a7, #43a047); font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .container { background: rgba(255,255,255,0.95); border-radius: 18px; box-shadow: 0 8px 32px rgba(67,160,71,0.12); padding: 32px 28px; display: flex; flex-direction: column; align-items: center; }
        h1 { color: #2e7d32; margin-bottom: 18px; letter-spacing: 2px; }
        form { display: flex; flex-direction: column; align-items: center; }
        input[type="file"] { margin-bottom: 18px; }
        button { background: #43a047; color: #fff; border: none; border-radius: 8px; padding: 10px 28px; font-size: 18px; cursor: pointer; transition: background 0.2s; }
        button:hover { background: #388e3c; }
        .result { margin-top: 24px; text-align: center; }
        .footer { margin-top: 32px; color: #A5D6A7; font-size: 14px; }
        img.preview { max-width: 180px; max-height: 180px; border-radius: 12px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(67,160,71,0.08); }
        .emotion-raw { font-size: 22px; color: #2e7d32; margin-top: 8px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sproutify Emotion Check</h1>
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
def index():
    emotion = None
    photo_url = None
    if request.method == 'POST':
        file = request.files.get('photo')
        if file:
            # Send the image to the backend API and get plain text response
            response = requests.post(
                'http://127.0.0.1:5001/detect',
                files={'image': (file.filename, file, file.content_type)}
            )
            if response.ok:
                emotion = response.text  # Use the raw response as-is
            else:
                emotion = 'Error contacting emotion API.'
            # For preview, we can use data URL (not for production, but fine for demo)
            import base64
            file.seek(0)
            img_bytes = file.read()
            photo_url = 'data:' + file.content_type + ';base64,' + base64.b64encode(img_bytes).decode('utf-8')
    return render_template_string(TEMPLATE, emotion=emotion, photo_url=photo_url)

if __name__ == '__main__':
    app.run(debug=True) 