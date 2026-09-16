import sqlite3
import pandas as pd
import math

print("Membaca loan_history.xlsx...")
df = pd.read_excel("loan_history.xlsx")
# Kolom: 'Member ID', 'Member Name', 'Item Code', 'Title', 'Loan Date', 'Due Date', 'Loan Status'

conn = sqlite3.connect("katalog.db")
cursor = conn.cursor()

# Buat tabel
cursor.execute('''
CREATE TABLE IF NOT EXISTS peminjaman (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id TEXT,
    member_name TEXT,
    no_induk TEXT,
    judul TEXT,
    loan_date TEXT,
    due_date TEXT,
    loan_status TEXT
)
''')
# Hapus data lama jika mau diclear tiap kali import
cursor.execute('DELETE FROM peminjaman')

print("Memasukkan data ke database...")
count = 0
for index, row in df.iterrows():
    no_induk = str(row['Item Code']) if pd.notna(row['Item Code']) else ''
    loan_date = str(row['Loan Date']) if pd.notna(row['Loan Date']) else ''
    
    cursor.execute('''
        INSERT INTO peminjaman (member_id, member_name, no_induk, judul, loan_date, due_date, loan_status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        str(row['Member ID']),
        str(row['Member Name']),
        no_induk,
        str(row['Title']),
        loan_date,
        str(row['Due Date']),
        str(row['Loan Status'])
    ))
    count += 1

conn.commit()
conn.close()
print(f"Berhasil mengimpor {count} data peminjaman!")
