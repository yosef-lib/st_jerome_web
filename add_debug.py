import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

debug_api = '''
@app.route('/api/debug/db_path', methods=['GET'])
def api_debug_db():
    import os
    import database
    return jsonify({
        'cwd': os.getcwd(),
        'db_path_relative': database.DB_NAME,
        'db_path_absolute': os.path.abspath(database.DB_NAME),
        'db_exists': os.path.exists(os.path.abspath(database.DB_NAME))
    })
'''
# append to end
code += debug_api

# Also I need to put back login_required to api_get_member because I accidentally removed it!
code = code.replace("@app.route('/api/sirkulasi/member/<member_id>', methods=['GET'])\ndef api_get_member(member_id):", "@app.route('/api/sirkulasi/member/<member_id>', methods=['GET'])\n@login_required\ndef api_get_member(member_id):")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Debug API added.")
