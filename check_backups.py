import os
import glob

def find_db_files():
    print("Mencari file database di server...")
    files = []
    # Search in current directory and /root
    for pattern in ['*.db', '*.sqlite3', '*.csv', '*backup*', '*katalog*']:
        files.extend(glob.glob(pattern))
        files.extend(glob.glob('/root/' + pattern))
        files.extend(glob.glob('/root/st_jerome_web/' + pattern))
        
    files = list(set(files))
    for f in files:
        try:
            size = os.path.getsize(f)
            print(f"- {f} (Ukuran: {size/1024:.2f} KB)")
        except:
            pass

find_db_files()
