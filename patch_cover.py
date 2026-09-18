import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

old_list = """        cursor = conn.execute(query, (f'%{search}%', f'%{search}%', f'%{search}%', per_page, offset))
        results = [dict(row) for row in cursor.fetchall()]"""

new_list = """        cursor = conn.execute(query, (f'%{search}%', f'%{search}%', f'%{search}%', per_page, offset))
        results = [dict(row) for row in cursor.fetchall()]
        
        import re
        for row in results:
            if row.get('image'):
                row['cover_url'] = f"/static/uploads/{row['image']}"
            elif row.get('isbn'):
                # Extract first clean ISBN (remove hyphens, non-alphanumeric except X)
                raw_isbn = str(row['isbn']).split(',')[0].split(' ')[0].upper()
                cleaned = re.sub(r'[^0-9X]', '', raw_isbn)
                if cleaned:
                    row['cover_url'] = f"https://covers.openlibrary.org/b/isbn/{cleaned}-M.jpg?default=false"
                else:
                    row['cover_url'] = None
            else:
                row['cover_url'] = None"""

code = code.replace(old_list, new_list)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Backend patched for cover_url")
