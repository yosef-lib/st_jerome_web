import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Fix 1: Make session permanent (survives browser close) and extend lifetime
old_secret = "app.secret_key = 'stjerome_secret_key'"
new_secret = """app.secret_key = 'stjerome_secret_key_imavi_2026'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 7  # 7 days"""

code = code.replace(old_secret, new_secret)

# Fix 2: Make session permanent on login
old_login = "session['logged_in'] = True"
new_login = "session.permanent = True\n            session['logged_in'] = True"
code = code.replace(old_login, new_login)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Session config fixed")
