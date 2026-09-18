import database
conn = database.get_db_connection()
rows = conn.execute("SELECT judul, pengarang, penerbit, COUNT(*) as c FROM buku GROUP BY judul, pengarang, penerbit HAVING c > 1 ORDER BY c DESC LIMIT 10").fetchall()
for r in rows:
    print(f"'{r[0]}' | '{r[1]}' | '{r[2]}' : {r[3]} copies")
