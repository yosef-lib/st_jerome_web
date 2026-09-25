import database
conn = database.get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM buku")
buku_rows = cursor.fetchall()
cursor.execute("PRAGMA table_info(buku)")
columns = [col[1] for col in cursor.fetchall()]

biblio_map = {}
for row in buku_rows:
    row_dict = dict(zip(columns, row))
    key = (row_dict.get('judul', ''), row_dict.get('pengarang', ''), row_dict.get('penerbit', ''))
    if key not in biblio_map:
        biblio_map[key] = row_dict.get('no_induk')
print(f"Total unique keys: {len(biblio_map)}")
