
import sqlite3

def test():
    conn = sqlite3.connect("katalog.db")
    conn.row_factory = sqlite3.Row
    search = "A"
    query = """
        SELECT b.id, b.judul, b.pengarang, b.penerbit, b.tahun_terbit, b.klasifikasi, b.image, b.isbn,
               COUNT(e.no_induk) as total_eksemplar,
               SUM(CASE WHEN e.status_ketersediaan = 'Tersedia' THEN 1 ELSE 0 END) as tersedia
        FROM bibliografi b
        LEFT JOIN eksemplar e ON b.id = e.biblio_id
        WHERE b.judul LIKE ? OR b.pengarang LIKE ? OR b.penerbit LIKE ? OR b.klasifikasi LIKE ?
        GROUP BY b.id
        ORDER BY b.id DESC
        LIMIT 1
    """
    try:
        cursor = conn.execute(query, (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%"))
        results = [dict(row) for row in cursor.fetchall()]
        print("SUCCESS:", results)
    except Exception as e:
        print("FAILED:", e)

test()

