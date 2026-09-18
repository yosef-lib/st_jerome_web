import sqlite3
import time
import urllib.request
import json
import urllib.parse
import sys

DB_PATH = 'katalog.db'

def get_db():
    return sqlite3.connect(DB_PATH)

def fetch_google_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if 'items' in data and len(data['items']) > 0:
                img = data['items'][0].get('volumeInfo', {}).get('imageLinks', {}).get('thumbnail')
                if img:
                    return img.replace('http:', 'https:')
            return 'NOT_FOUND'
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return 'RATE_LIMIT'
        return 'NOT_FOUND'
    except Exception as e:
        print(f"Request error: {e}")
        return 'ERROR'

def run_robot():
    print("=========================================")
    print("?? Robot Pencari Sampul (Mode Latar Belakang)")
    print("=========================================")
    
    conn = get_db()
    total_left = conn.execute("SELECT COUNT(*) FROM bibliografi WHERE image IS NULL OR image = ''").fetchone()[0]
    conn.close()
    
    print(f"Total buku yang akan diperiksa: {total_left}")
    
    while True:
        try:
            conn = get_db()
            cursor = conn.execute("SELECT id, judul, pengarang FROM bibliografi WHERE image IS NULL OR image = '' LIMIT 20")
            books = cursor.fetchall()
            
            if not books:
                print("Hore! Semua buku sudah selesai diproses.")
                conn.close()
                time.sleep(3600)
                continue
                
            for b in books:
                b_id, judul, pengarang = b
                print(f"Mencari: {judul[:40]}...", end=" ", flush=True)
                
                q = f"intitle:{judul}"
                if pengarang:
                    q += f"+inauthor:{pengarang}"
                    
                img_url = fetch_google_books(q)
                
                if img_url == 'RATE_LIMIT':
                    print("[TERKENA LIMIT GOOGLE! Istirahat 2 menit...]")
                    time.sleep(120)
                    break
                elif img_url == 'ERROR':
                    print("[ERROR KONEKSI]")
                    time.sleep(5)
                else:
                    if img_url == 'NOT_FOUND':
                        print("Tidak Ditemukan.")
                    else:
                        print("DAPAT!")
                    
                    conn.execute("UPDATE bibliografi SET image = ? WHERE id = ?", (img_url, b_id))
                    conn.commit()
                    time.sleep(2) # 2 seconds sleep between requests to avoid rate limit
                    
            conn.close()
            time.sleep(1)
        except Exception as e:
            print(f"Fatal error: {e}")
            time.sleep(10)

if __name__ == '__main__':
    run_robot()
