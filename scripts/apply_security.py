import os
import re

app_file = 'app.py'
with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Cookie config and Secret Key
import secrets
new_secret_setup = '''
# === Security Config (Anti-CSRF & Secret Key) ===
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True # Untuk HTTPS

import secrets
def get_or_create_secret_key():
    import database
    conn = database.get_db_connection()
    try:
        row = conn.execute("SELECT nilai FROM pengaturan_sistem WHERE kunci = 'FLASK_SECRET_KEY'").fetchone()
        if row and row['nilai']:
            key = row['nilai']
        else:
            key = secrets.token_hex(32)
            conn.execute("INSERT OR REPLACE INTO pengaturan_sistem (kunci, nilai) VALUES (?, ?)", ('FLASK_SECRET_KEY', key))
            conn.commit()
    except Exception as e:
        key = secrets.token_hex(32)
    finally:
        conn.close()
    return key

app.secret_key = get_or_create_secret_key()
# ================================================

'''
content = re.sub(r"app\.secret_key = 'stjerome_secret_key_imavi_2026'", new_secret_setup, content)

# 2. Add File Upload Validation
upload_filter = '''
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg', 'webp'}
def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE
'''
content = content.replace("app = Flask(__name__)", "app = Flask(__name__)\n" + upload_filter)

# Apply filter to api_input_batch
batch_replace_old = '''    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            filename = secure_filename(file.filename)'''
batch_replace_new = '''    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_image(file.filename):
            filename = secure_filename(file.filename)'''
content = content.replace(batch_replace_old, batch_replace_new)

# Apply filter to manual upload in /koleksi/edit/<int:id> if exists
# Wait, I didn't see an image upload in edit_koleksi, only input_batch.

with open(app_file, 'w', encoding='utf-8') as f:
    f.write(content)
