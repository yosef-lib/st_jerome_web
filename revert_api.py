import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace("@app.route('/api/sirkulasi/member/<member_id>', methods=['GET'])", "@app.route('/api/sirkulasi/member/<member_id>', methods=['GET'])\n@login_required")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Reverted login_required")
