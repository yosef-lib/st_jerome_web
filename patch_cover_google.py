import codecs

with codecs.open('app.py', 'r', 'utf-8') as f:
    code = f.read()

old_cover = "row['cover_url'] = f\"https://covers.openlibrary.org/b/isbn/{cleaned}-M.jpg?default=false\""
new_cover = "row['cover_url'] = f\"https://books.google.com/books/content?vid=ISBN{cleaned}&printsec=frontcover&img=1&zoom=1\""
code = code.replace(old_cover, new_cover)

with codecs.open('app.py', 'w', 'utf-8') as f:
    f.write(code)
print("Switched to Google Books API")
