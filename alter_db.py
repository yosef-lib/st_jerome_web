from database import get_db_connection

conn = get_db_connection()
try:
    conn.execute("ALTER TABLE buku ADD COLUMN gambar_sampul TEXT")
    conn.commit()
    print("Column added")
except Exception as e:
    print(e)
conn.close()
