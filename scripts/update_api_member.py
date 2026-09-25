import codecs
import re

with codecs.open('app.py', 'r', 'utf-8') as f:
    app_code = f.read()

old_block = '''    conn.close()
    return jsonify({
        'status': 'success',
        'data': {
            'id': m['member_id'],
            'nama': m['nama'],
            'tipe': tipe,
            'status': m['status'],
            'suspended_until': m.get('suspended_until', '-'),
            'active_loans': active_loans,
            'max_loans': max_loans
        }
    })'''

new_block = '''    # Fetch active loans detail
    loans_cursor = conn.execute("""
        SELECT s.*, e.no_induk, b.judul 
        FROM sirkulasi s
        JOIN eksemplar e ON s.no_induk = e.no_induk
        JOIN bibliografi b ON e.biblio_id = b.id
        WHERE s.member_id = ? AND s.return_date IS NULL
    """, (member_id,))
    loans = [dict(row) for row in loans_cursor.fetchall()]

    conn.close()
    return jsonify({
        'status': 'success',
        'data': {
            'id': m['member_id'],
            'nama': m['nama'],
            'tipe': tipe,
            'status': m['status'],
            'email': m.get('email', '-'),
            'masa_berlaku': m.get('masa_berlaku', '2027-05-07'),
            'suspended_until': m.get('suspended_until', '-'),
            'active_loans': active_loans,
            'max_loans': max_loans,
            'loans': loans
        }
    })'''

app_code = app_code.replace(old_block, new_block)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(app_code)
print("Updated api_get_member")
