import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

old_image = """        for row in results:
            if row.get('image'):
                row['cover_url'] = f"/static/uploads/{row['image']}\""""

new_image = """        for row in results:
            if row.get('image'):
                if row['image'].startswith('http'):
                    row['cover_url'] = row['image']
                else:
                    row['cover_url'] = f"/static/uploads/{row['image']}\""""

code = code.replace(old_image, new_image)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("app.py patched for http images")
