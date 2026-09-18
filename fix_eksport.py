import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

old_eksport = '''def eksport_stpd():
    import csv, io
    conn = database.get_db_connection()'''

new_eksport = '''def eksport_stpd():
    import csv, io
    from flask import Response
    conn = database.get_db_connection()'''

code = code.replace(old_eksport, new_eksport)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
