import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Add a new decorator specifically for API routes that returns JSON, not HTML redirect
new_decorator = '''def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return jsonify({'status': 'error', 'message': 'Sesi tidak valid, silakan refresh halaman.'}), 401
        return f(*args, **kwargs)
    return decorated_function

'''

# Insert after login_required
old_def = '''def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function'''

code = code.replace(old_def, old_def + '\n\n' + new_decorator)

# Replace @login_required with @api_login_required for all /api/ routes
import re

# Find all API route-function pairs and replace their decorator
def replace_api_decorator(text):
    # Replace @login_required right after @app.route('/api/...)
    pattern = r"(@app\.route\('/api/[^']*'[^\n]*\n)(@login_required\n)"
    return re.sub(pattern, lambda m: m.group(1) + m.group(2).replace('@login_required', '@api_login_required'), text)

code = replace_api_decorator(code)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("API auth fixed")
