import sqlite3
import pandas as pd

conn = sqlite3.connect('katalog.db')

query = '''
WITH Copies AS (
    SELECT judul, pengarang, klasifikasi, COUNT(no_induk) as total_eksemplar
    FROM buku
    WHERE lokasi = 'STPD'
    GROUP BY judul, pengarang
    HAVING total_eksemplar = 1
),
InHouseReads AS (
    SELECT b.judul, COUNT(bd.id) as read_count
    FROM buku_dibaca bd
    JOIN buku b ON bd.no_induk = b.no_induk
    WHERE b.lokasi = 'STPD'
    GROUP BY b.judul
),
ExternalLoans AS (
    SELECT p.Judul as judul, COUNT(p.id) as loan_count
    FROM peminjaman p
    GROUP BY p.Judul
)
SELECT 
    c.judul, 
    c.pengarang,
    c.klasifikasi,
    c.total_eksemplar,
    COALESCE(i.read_count, 0) as read_count,
    COALESCE(e.loan_count, 0) as loan_count,
    (COALESCE(i.read_count, 0) + COALESCE(e.loan_count, 0)) as total_usage
FROM Copies c
LEFT JOIN InHouseReads i ON c.judul = i.judul
LEFT JOIN ExternalLoans e ON c.judul = e.judul
WHERE total_usage > 0
ORDER BY total_usage DESC
LIMIT 10
'''

try:
    df = pd.read_sql_query(query, conn)
    print(df.head())
except Exception as e:
    print("Error:", e)
