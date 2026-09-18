import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# Check if /sirkulasi route exists
if "@app.route('/sirkulasi')" not in app_code:
    new_route = '''
@app.route('/sirkulasi')
@login_required
def sirkulasi():
    return render_template('sirkulasi.html', page_title="Sirkulasi & Kasir")
'''
    # Append it before the if __name__ == '__main__': block
    app_code = app_code.replace("if __name__ == '__main__':", new_route + "\nif __name__ == '__main__':")
    
    with codecs.open('app.py', 'w', 'utf-8') as f:
        f.write(app_code)
    print("Added /sirkulasi route to app.py")
else:
    print("/sirkulasi route already exists")
