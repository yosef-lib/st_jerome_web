import csv
import sqlite3

def import_anggota():
    conn = sqlite3.connect('katalog.db')
    conn.execute('DELETE FROM anggota')
    
    count = 0
    with open('senayan_member_export.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) < 10:
                continue
            
            member_id = row[0]
            nama = row[1]
            tipe = row[3]
            email = row[4]
            alamat = row[5]
            institusi = row[7]
            telepon = row[11] if len(row) > 11 else ''
            masa_berlaku = row[15] if len(row) > 15 else ''
            
            try:
                conn.execute('''
                    INSERT INTO anggota (member_id, nama, tipe_anggota, institusi, email, telepon, alamat, masa_berlaku)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (member_id, nama, tipe, institusi, email, telepon, alamat, masa_berlaku))
                count += 1
            except sqlite3.IntegrityError:
                pass
                
    conn.commit()
    conn.close()
    print(f"Berhasil impor {count} anggota.")

if __name__ == '__main__':
    import_anggota()
