
import sqlite3
conn = sqlite3.connect("test_katalog.db")
search = "Allah"
query = """
        SELECT b.id, b.judul, b.pengarang, b.penerbit, b.tahun_terbit, b.klasifikasi, b.image, b.isbn,
               COUNT(e.no_induk) as total_eksemplar,
               SUM(CASE WHEN e.status_ketersediaan = "Tersedia" THEN 1 ELSE 0 END) as tersedia
        FROM bibliografi b
        LEFT JOIN eksemplar e ON b.id = e.biblio_id
        WHERE b.judul LIKE ? OR b.pengarang LIKE ? OR b.penerbit LIKE ? OR b.klasifikasi LIKE ?
        GROUP BY b.id
        ORDER BY b.id DESC
        LIMIT 50
"""
try:
    cursor = conn.execute(query, (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")

