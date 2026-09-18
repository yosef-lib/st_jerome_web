import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

new_api = '''@app.route('/api/ddc/search', methods=['GET'])
@login_required
def api_ddc_search():
    keyword = request.args.get('q', '').lower()
    import json
    try:
        with open('ddc_kamus.json', 'r') as f:
            ddc_dict = json.load(f)
    except:
        ddc_dict = {}
        
    results = []
    
    # Clean keywords (ignore short words)
    ignore_words = ['pengantar', 'buku', 'panduan', 'dasar', 'teori', 'ilmu', 'dan', 'yang']
    keywords = [w for w in keyword.split() if w not in ignore_words and len(w) > 2]
    
    # If no keywords left, just search the original keyword
    if not keywords:
        keywords = [keyword]
        
    for code, desc in ddc_dict.items():
        # exact match
        if keyword in desc.lower():
            results.append({'kode': code, 'deskripsi': desc})
            continue
            
        # keyword match
        for kw in keywords:
            if kw in desc.lower():
                results.append({'kode': code, 'deskripsi': desc})
                break
                
    return jsonify(results)
'''

code = re.sub(r"@app\.route\('/api/ddc/search'.*?return jsonify\(results\)", new_api, code, flags=re.DOTALL)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("DDC search updated.")
