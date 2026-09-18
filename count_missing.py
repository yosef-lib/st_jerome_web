import database

conn = database.get_db_connection()

total_biblio = conn.execute("SELECT COUNT(*) FROM bibliografi").fetchone()[0]
has_image = conn.execute("SELECT COUNT(*) FROM bibliografi WHERE image IS NOT NULL AND image != ''").fetchone()[0]
has_isbn = conn.execute("SELECT COUNT(*) FROM bibliografi WHERE isbn IS NOT NULL AND isbn != ''").fetchone()[0]
no_isbn_no_image = conn.execute("SELECT COUNT(*) FROM bibliografi WHERE (isbn IS NULL OR isbn = '') AND (image IS NULL OR image = '')").fetchone()[0]

print(f"Total Judul Buku (Bukan Salinan): {total_biblio}")
print(f"Buku dengan ISBN (Dicari Otomatis oleh Google): {has_isbn}")
print(f"Buku tanpa ISBN & tanpa Foto (Logo Abu-abu Pasti): {no_isbn_no_image}")

conn.close()
