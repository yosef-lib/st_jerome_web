import codecs, re

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

pattern = r"@app\.route\('/api/antrean/hapus', methods=\['POST'\]\)\s*@login_required\s*def hapus_antrean\(\):.*?return jsonify\(\{'status': 'success'\}\)"
new_func = '''@app.route('/api/antrean/hapus', methods=['POST'])
@login_required
def hapus_antrean():
    no_induk = request.json.get('no_induk')
    index = request.json.get('index')
    
    if os.path.exists(ANTREAN_FILE):
        import json
        with open(ANTREAN_FILE, 'r') as f:
            try:
                queue = json.load(f)
            except:
                queue = []
                
        if no_induk:
            queue = [b for b in queue if str(b.get('no_induk', '')) != str(no_induk)]
        elif index is not None and 0 <= index < len(queue):
            queue.pop(index)
            
        with open(ANTREAN_FILE, 'w') as f:
            json.dump(queue, f)
            
    return jsonify({'status': 'success'})'''

app_code, count = re.subn(pattern, new_func, app_code, flags=re.DOTALL)
print(f"Replaced {count} times")

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)
