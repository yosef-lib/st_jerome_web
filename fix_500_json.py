import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

handler = '''
@app.errorhandler(500)
def internal_error(error):
    import traceback
    return jsonify({
        'status': 'error', 
        'message': 'Internal Server Error: ' + str(error),
        'trace': traceback.format_exc()
    }), 500

'''

code = code.replace("app = Flask(__name__)", "app = Flask(__name__)\n" + handler)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("500 handler added")
