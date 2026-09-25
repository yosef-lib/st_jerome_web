from flask import Flask, jsonify
import traceback

app = Flask(__name__)

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error', 
        'message': 'Internal Server Error: ' + str(error),
        'trace': traceback.format_exc()
    }), 500

@app.route('/')
def index():
    raise ValueError("Test error")

client = app.test_client()
print(client.get('/').get_json())
