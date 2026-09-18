import sqlite3

def migrate():
    conn = sqlite3.connect('katalog.db')
    cursor = conn.cursor()
    
    # 1. Update buku table
    try:
        cursor.execute("ALTER TABLE buku ADD COLUMN is_reference_only INTEGER DEFAULT 0;")
        print("Column is_reference_only added to buku.")
    except sqlite3.OperationalError as e:
        print(f"buku already has column or error: {e}")

    # 2. Update anggota table
    try:
        cursor.execute("ALTER TABLE anggota ADD COLUMN status TEXT DEFAULT 'AKTIF';")
        cursor.execute("ALTER TABLE anggota ADD COLUMN suspended_until TEXT;")
        print("Columns status, suspended_until added to anggota.")
    except sqlite3.OperationalError as e:
        print(f"anggota already has column or error: {e}")

    # 3. Create sirkulasi table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sirkulasi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id TEXT,
        no_induk TEXT,
        loan_date TEXT,
        due_date TEXT,
        return_date TEXT,
        renewal_count INTEGER DEFAULT 0,
        fine_amount INTEGER DEFAULT 0,
        fine_status TEXT DEFAULT 'BELUM_LUNAS'
    )
    ''')
    print("Table sirkulasi ensured.")

    # 4. Create hari_libur table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hari_libur (
        tanggal TEXT PRIMARY KEY,
        keterangan TEXT
    )
    ''')
    print("Table hari_libur ensured.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()
