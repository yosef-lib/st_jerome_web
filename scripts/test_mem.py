
import sqlite3
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE bibliografi (id INTEGER PRIMARY KEY, judul TEXT, pengarang TEXT, penerbit TEXT, tahun_terbit TEXT, klasifikasi TEXT, image TEXT, isbn TEXT)")
conn.execute("CREATE TABLE eksemplar (no_induk TEXT, biblio_id INTEGER, status_ketersediaan TEXT)")
query = """SELECT b.id, b.judul, b.pengarang, b.penerbit, b.tahun_terbit, b.klasifikasi, b.image, b.isbn,
               COUNT(e.no_induk) as total_eksemplar,
               SUM(CASE WHEN e.status_ketersediaan = 'Tersedia' THEN 1 ELSE 0 END) as tersedia
        FROM bibliografi b
        LEFT JOIN eksemplar e ON b.id = e.biblio_id
        WHERE b.judul LIKE ? OR b.pengarang LIKE ? OR b.penerbit LIKE ? OR b.klasifikasi LIKE ?
        GROUP BY b.id
        ORDER BY b.id DESC
        LIMIT 50"""
try:
    conn.execute(query, ("%A%", "%A%", "%A%", "%A%"))
    print("SUCCESS")
except Exception as e:
    print("FAILED:", e)

