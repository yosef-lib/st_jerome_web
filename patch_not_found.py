import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

# Update missing_covers query to exclude 'NOT_FOUND'
old_q = "cursor = conn.execute(\"SELECT id, judul, pengarang FROM bibliografi WHERE (isbn IS NULL OR isbn = '') AND (image IS NULL OR image = '') LIMIT 100\")"
new_q = "cursor = conn.execute(\"SELECT id, judul, pengarang FROM bibliografi WHERE (isbn IS NULL OR isbn = '') AND (image IS NULL OR image = '') LIMIT 50\")"
code = code.replace(old_q, new_q)

old_logic = """        for row in results:
            if row.get('image'):
                if row['image'].startswith('http'):
                    row['cover_url'] = row['image']
                else:
                    row['cover_url'] = f"/static/uploads/{row['image']}\""""

new_logic = """        for row in results:
            if row.get('image'):
                if row['image'] == 'NOT_FOUND':
                    row['cover_url'] = None
                elif row['image'].startswith('http'):
                    row['cover_url'] = row['image']
                else:
                    row['cover_url'] = f"/static/uploads/{row['image']}\""""
code = code.replace(old_logic, new_logic)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)

with codecs.open('templates/koleksi.html', 'r', 'utf-8') as f:
    html = f.read()

old_js = """                                if(img) {
                                    // replace http with https
                                    img = img.replace("http:", "https:");
                                    await fetch('/api/buku/save_cover', {
                                        method: 'POST',
                                        headers: {'Content-Type': 'application/json'},
                                        body: JSON.stringify({id: b.id, url: img})
                                    });
                                }"""

new_js = """                                if(img) {
                                    img = img.replace("http:", "https:");
                                    await fetch('/api/buku/save_cover', {
                                        method: 'POST', headers: {'Content-Type': 'application/json'},
                                        body: JSON.stringify({id: b.id, url: img})
                                    });
                                } else {
                                    await fetch('/api/buku/save_cover', {
                                        method: 'POST', headers: {'Content-Type': 'application/json'},
                                        body: JSON.stringify({id: b.id, url: 'NOT_FOUND'})
                                    });
                                }
                            } else {
                                await fetch('/api/buku/save_cover', {
                                    method: 'POST', headers: {'Content-Type': 'application/json'},
                                    body: JSON.stringify({id: b.id, url: 'NOT_FOUND'})
                                });
                            }
                        } else {
                            await fetch('/api/buku/save_cover', {
                                method: 'POST', headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({id: b.id, url: 'NOT_FOUND'})
                            });
                        }"""
html = html.replace(old_js, new_js)

with codecs.open('templates/koleksi.html', 'w', 'utf-8') as f:
    f.write(html)
print("Infinite loop prevented")
