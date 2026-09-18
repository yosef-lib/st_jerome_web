import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

# Replace the first /cetak_kartu (my new one) with /cetak_sirkulasi
# I can just replace the definition block I added.
old_block = '''@app.route('/cetak_kartu')
@login_required
def cetak_kartu():
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))'''

new_block = '''@app.route('/cetak_sirkulasi')
@login_required
def cetak_sirkulasi():
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))'''

app_code = app_code.replace(old_block, new_block)

old_api = '''@app.route('/api/cetak_kartu', methods=['POST'])
@login_required
def api_cetak_kartu():'''

new_api = '''@app.route('/api/cetak_sirkulasi', methods=['POST'])
@login_required
def api_cetak_sirkulasi():'''

app_code = app_code.replace(old_api, new_api)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)

# Rename the HTML file
import os
if os.path.exists('templates/cetak_kartu.html'):
    os.rename('templates/cetak_kartu.html', 'templates/cetak_sirkulasi.html')

# Update layout.html to point to /cetak_sirkulasi
with codecs.open('templates/layout.html', 'r', 'utf-8') as f:
    layout = f.read()
layout = layout.replace('/cetak_kartu', '/cetak_sirkulasi')
with codecs.open('templates/layout.html', 'w', 'utf-8') as f:
    f.write(layout)
    
# Update JS inside cetak_sirkulasi.html
with codecs.open('templates/cetak_sirkulasi.html', 'r', 'utf-8') as f:
    html = f.read()
html = html.replace('/api/cetak_kartu', '/api/cetak_sirkulasi')
html = html.replace('/cetak_kartu', '/cetak_sirkulasi')
with codecs.open('templates/cetak_sirkulasi.html', 'w', 'utf-8') as f:
    f.write(html)
