import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Add version endpoint to confirm latest code
version_api = '''
@app.route('/api/version', methods=['GET'])
def api_version():
    return jsonify({'version': '2b2fa3d-fix-401', 'status': 'ok'})
'''

code += version_api

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Version endpoint added")
