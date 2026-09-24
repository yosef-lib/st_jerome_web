import os
import sqlite3
import zipfile
import datetime
import urllib.request
import urllib.parse
import json

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'katalog.db')

def get_config():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        token_row = conn.execute("SELECT nilai FROM pengaturan_sistem WHERE kunci = 'TELEGRAM_BOT_TOKEN'").fetchone()
        chat_id_row = conn.execute("SELECT nilai FROM pengaturan_sistem WHERE kunci = 'TELEGRAM_CHAT_ID'").fetchone()
        conn.close()
        
        token = token_row['nilai'] if token_row else None
        chat_id = chat_id_row['nilai'] if chat_id_row else None
        return token, chat_id
    except Exception as e:
        print("Error reading config:", e)
        return None, None

def run_backup(manual=False):
    token, chat_id = get_config()
    if not token or not chat_id:
        return False, "Telegram Token atau Chat ID belum dikonfigurasi."
        
    if not os.path.exists(DB_PATH):
        return False, "Database tidak ditemukan."

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"backup_stjerome_{timestamp}.zip"
    zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), zip_filename)
    
    try:
        # 1. Zip the database and uploads directory
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(DB_PATH, arcname='katalog.db')
            
            uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
            if os.path.exists(uploads_dir):
                for root, dirs, files in os.walk(uploads_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.join('static', 'uploads', os.path.relpath(file_path, uploads_dir))
                        zipf.write(file_path, arcname=arcname)
            
        # 2. Send via Telegram API
        url = f"https://api.telegram.org/bot{token}/sendDocument"
        
        # We have to use multipart/form-data to upload the file.
        # Since we don't have requests installed explicitly (though Flask relies on Werkzeug which can do it, or we use urllib)
        # To avoid dependencies, let's use a simple shell curl command if on linux, or requests if available.
        # Let's try importing requests
        import requests
        
        with open(zip_path, 'rb') as f:
            files = {'document': (zip_filename, f, 'application/zip')}
            data = {
                'chat_id': chat_id,
                'caption': f"?? *Backup St. Jerome Library*\n\nTanggal: {datetime.datetime.now().strftime('%d %b %Y %H:%M')}\nStatus: {'Manual Backup' if manual else 'Auto Backup (Harian)'}",
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, data=data, files=files, timeout=30)
            
        if response.status_code == 200:
            os.remove(zip_path) # Clean up the zip file
            return True, "Backup berhasil dikirim ke Telegram."
        else:
            return False, f"Gagal mengirim. Kode: {response.status_code}, Response: {response.text}"
            
    except ImportError:
        return False, "Library requests tidak ditemukan. Jalankan 'pip install requests'"
    except Exception as e:
        return False, str(e)
    finally:
        # Cleanup zip if it still exists and we failed
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except:
                pass

if __name__ == "__main__":
    print("Memulai proses backup...")
    success, msg = run_backup()
    print(f"[{'SUCCESS' if success else 'FAILED'}] {msg}")
