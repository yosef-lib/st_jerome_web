import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

code = code.replace("@app.route('/api/eksemplar/<string:no_induk>', methods=['DELETE'])", "@app.route('/api/eksemplar/<path:no_induk>', methods=['DELETE'])")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Route updated to <path:no_induk>")
