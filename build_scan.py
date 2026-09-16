import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    content = f.read()

old_scan = '''@app.route('/api/scan', methods=['POST'])
def api_scan():
    no_induk = request.json.get('no_induk')
    if not no_induk:
        return jsonify({'status': 'error', 'message': 'No Induk kosong'}), 400
        
    conn = database.get_db_connection()
    buku = conn.execute('SELECT * FROM buku WHERE no_induk = ?', (no_induk,)).fetchone()
    
    if buku:
        try:
            conn.execute('INSERT INTO buku_dibaca (no_induk) VALUES (?)', (no_induk,))
            return jsonify({
                'status': 'success', 
                'message': f'Buku {buku["judul"]} berhasil dicatat!',
                'buku': dict(buku)
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Buku tidak ditemukan di database.'}), 404'''

new_scan = '''@app.route('/api/scan', methods=['POST'])
def api_scan():
    no_induk = request.json.get('no_induk')
    mode = request.json.get('mode', 'meja_baca') # 'meja_baca' atau 'audit_rak'
    target_rak = request.json.get('target_rak', '') # e.g. '200'
    
    if not no_induk:
        return jsonify({'status': 'error', 'message': 'No Induk kosong'}), 400
        
    conn = database.get_db_connection()
    buku = conn.execute('SELECT * FROM buku WHERE no_induk = ?', (no_induk,)).fetchone()
    
    if buku:
        if mode == 'meja_baca':
            try:
                conn.execute('INSERT INTO buku_dibaca (no_induk) VALUES (?)', (no_induk,))
                return jsonify({
                    'status': 'success', 
                    'message': f'Buku {buku["judul"]} berhasil dicatat!',
                    'buku': dict(buku)
                })
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 500
        elif mode == 'audit_rak':
            klasifikasi = buku['klasifikasi']
            if not klasifikasi:
                return jsonify({
                    'status': 'warning',
                    'message': f'Buku "{buku["judul"]}" tidak memiliki DDC (Anomali Metadata).',
                    'buku': dict(buku)
                })
            
            ddc_awal = klasifikasi[0] + '00' # e.g. '2' -> '200'
            if ddc_awal == target_rak:
                return jsonify({
                    'status': 'success',
                    'message': f'BENAR: Buku "{buku["judul"]}" (DDC {klasifikasi}) berada di rak yang tepat.',
                    'buku': dict(buku)
                })
            else:
                return jsonify({
                    'status': 'danger',
                    'message': f'SALAH RAK! Buku "{buku["judul"]}" (DDC {klasifikasi}) seharusnya di Rak {ddc_awal}.',
                    'buku': dict(buku)
                })
    else:
        return jsonify({'status': 'error', 'message': 'Buku tidak ditemukan di database.'}), 404'''

content = content.replace(old_scan, new_scan)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(content)
print("api_scan updated")
